"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

#!/usr/local/bin/python
# -*- coding: utf-8 -*-


"""
This module provides a WaveUploader object to upload the saved csv data into Wave platform.
"""
import os
import subprocess
import urllib
from urllib import request
import json
import base64
import time
import sys
from datetime import datetime, timedelta
from wave_common import utils
from wave_common import JsonUtils

MB_CONVERSION = 1024*1024
SEGMENT_MEGABYTES = 8 * MB_CONVERSION

def erroCsv(csvFile):
    """
    Rename the csv file with err notation
    :param csvFile: input csv file name
    :return: new file name
    """
    return csvFile.replace('.csv', '_err.csv')

def schemaFile(csvFile):
    """
    Rename the csv file with schema notation and change to json file
    :param csvFile: input csv file name
    :return: new file name
    """
    return csvFile.replace('.csv', '_schema.json')

class WaveUploader:
    def __init__(self, wave_connector, data_set_id, dataset, mode, dataConfig, setup):
        # self._loginInfo = loginInfo
        self._dataConfig = dataConfig
        self._dataset_id = data_set_id
        self._dataset = dataset
        self._mode = mode
        self._setup = setup
        self._wave_connector = wave_connector

    def moveFiles(self, files, destinationFolder):
        """
        Move the list of files into the target folder.
        :param files: a list of files
        :param destinationFolder: target folder
        :return: return False if any error happens else return True
        """
        for fileElement in files:
            returnCode = subprocess.call(
                ['/bin/mv', fileElement, destinationFolder])
            if returnCode > 0:
                info = "Can not move " + fileElement + \
                    " return code:" + str(returnCode)
                print(info)
                return returnCode
        return 0

    def removeLocalFiles(self):
        # remove gz and previous data schema json and old csvs
        subprocess.call(
            '/bin/rm ' +
            self._dataConfig.dataFolder +
            "/*.json",
            shell=True)
        subprocess.call(
            '/bin/rm ' +
            self._dataConfig.dataFolder +
            "/*.gz",
            shell=True)

    def moveSuccessFiles(self, successFiles):
        filesToMove = []
        for f in successFiles:
            csvFile = self._dataConfig.dataFolder + "/" + f
            filesToMove.append(csvFile)

        returnCode = self.moveFiles(filesToMove, self._dataConfig.doneFolder)

        if returnCode > 0:
            info = 'Fail to move completed files:' + ",".join(filesToMove)
            print(info)
            return False
        else:
            print('Move success files completed: ' + ",".join(filesToMove))

    def uploadToWave(self, toBeProcessedFile, access_token):
        """
        throw HttpError to be caught
        :param toBeProcessedFile:
        :param access_token:
        :return:
        """
        print('uploading .....%s' % toBeProcessedFile)

        #create an InsightsExternalData object
        base64_meta_json = None

        metaJSONdata = self._metadata_for_dataset(toBeProcessedFile)

        if metaJSONdata is not None:
            base64_meta_json = base64.b64encode(bytearray(metaJSONdata, 'UTF-8'))

        insight_object_data = {
            "Format": "Csv",
            "EdgemartAlias": self._dataset,
            "Operation": self._mode,
            "Action": "none",
            "MetadataJson": base64_meta_json.decode() if base64_meta_json is not None else ''
        }
        # JsonUtils.pretty_print(insight_object_data)
        # insight_object_data = json.dumps(insight_object_data)
        headers = {'Authorization': 'Bearer ' + access_token, 
                    'Content-Type': 'application/json'}

        insight_object_parent_id = self._wave_connector.postInsightsExternalData(insight_object_data)

        #no need to convert metadata since the file is already uploaded to the dataset when it was created
        file_size_in_mb = float(os.path.getsize(toBeProcessedFile))/float(MB_CONVERSION)
        print(str(file_size_in_mb) + ' MB')

        #if file is > 8 MB then split the file
        if( file_size_in_mb > 8):
            fileparts = self.splitFile(toBeProcessedFile)
            for i in range(len(fileparts)):
                base64data = fileparts[i]
                json_content = {
                    "DataFile": base64data.decode('ascii'),
                    "InsightsExternalDataId": insight_object_parent_id,
                    "PartNumber": i+1
                }
                req = request.Request(self._request_external_data_part_url(), headers=headers, data=json.dumps(json_content).encode('ascii'))
                with request.urlopen(req) as response:
                    insight_part_response = response.read()
                    insight_object_response = json.loads(insight_part_response)
                    if('id' not in insight_object_response):
                        raise Exception('Something went wrong with creating the InsightsExternalData object -- see error: ' +
                            str(insight_part_response))

        else:
            data = utils.read_file(toBeProcessedFile)
            # with open(toBeProcessedFile, 'r') as f:
            #     data = f.read()

            base64data = base64.b64encode(bytearray(data, 'UTF-8'))

            json_content = {
                "DataFile": base64data.decode('ascii'),
                "InsightsExternalDataId": insight_object_parent_id,
                "PartNumber": 1
            }

            req = request.Request(self._request_external_data_part_url(), headers=headers, data=json.dumps(json_content).encode('ascii'))
            with request.urlopen(req) as response:
                insight_part_response = response.read()
                print('POST done')
                insight_object_response = json.loads(insight_part_response)
                if('id' not in insight_object_response):
                    raise Exception('Something went wrong with creating the InsightsExternalData object -- see error: ' +
                        str(response.read()))

        self.send_data_request(headers, insight_object_parent_id)

    def _metadata_for_dataset(self, csv_name):
        """
        search metadata file under metadata folder, if found, replace name with csvname
        :param csv_name: csv file name
        :return: meta data file under metadata folder
        """
        json_file = "metadata_template_" + self._dataset + ".json"
        # remove folder path, remove file extension, replace - with _
        csv_name = csv_name.split("/")[4]
        csv_name = csv_name.replace(".csv", "")
        csv_name = csv_name.replace("-", "_")

        path =  os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/../metadata"
        filedir = os.path.join(path, json_file)

        print(filedir)

        if not os.path.isfile(filedir):
            return None

        with open(filedir, 'r') as f:
            data = json.load(f)
            data["objects"][0]["fullyQualifiedName"] = "X" + csv_name
            data["objects"][0]["name"] = "X" + csv_name
            data["objects"][0]["label"] = "X" + csv_name
            data["objects"][0]["description"] = "X" + csv_name

        return json.dumps(data)

    def _request_url(self):
         return self._wave_connector.get_api_url() + self._setup.resource_url

    def _request_external_data_url(self):
        return self._request_url() + "/sobjects/InsightsExternalData/"

    def _request_external_data_part_url(self):
            return self._request_url() + "/sobjects/InsightsExternalDataPart/"

    def send_data_request(self, headers, parentId):
        print('request process')
        send_data_url = self._request_external_data_url() + parentId
        data = {
            "Action": "Process"
        }
        try:
            req = request.Request(send_data_url, headers=headers, data=json.dumps(data).encode('ascii'), method='PATCH')
            request.urlopen(req)
        except urllib.error.HTTPError as e:
            raise Exception('' + str(e.code) + " " + str(e.read()))

    def splitFile(self, toBeProcessedFile):
        fileparts = []

        with open(toBeProcessedFile, 'r') as f:
            byte = f.read(SEGMENT_MEGABYTES)
            while byte != "":
                encoded_str = base64.b64encode(bytes(byte, "UTF-8")) #converting to a base64 string
                fileparts.append(encoded_str)
                byte = f.read(SEGMENT_MEGABYTES) #reading the file 10mb at a time
        return fileparts

    def checkStatus(self, access_token, dataset_id):
        if dataset_id is None:
            raise Exception("please provide dataset_id for status check")

        url = self._request_url() + "/wave/datasets/" + dataset_id
        headers = {'Authorization': 'Bearer ' + access_token}
        counter = 0

        while counter <= 300:  #timeout after 5 minutes
            try:
                print('check dataset status %d'%counter)
                req = request.Request(url, headers=headers)
                with request.urlopen(req) as response:
                    content = response.read()
                    response_json = json.loads(content)
                    # print(content)

                    if("lastModifiedDate" not in response_json):
                        raise Exception('Something went wrong with making the request -- see error: ' + str(insight_part_response))

                    last_modified_date = response_json["lastModifiedDate"]

                    last_modified_date_split = last_modified_date.split("T")
                    last_modified_date = last_modified_date_split[0]
                    last_modified_time = last_modified_date_split[1]
                    last_modified_time = last_modified_time.split(".")[0]

                    last_modified_date = last_modified_date + "T" + last_modified_time
                    last_modified_date = datetime.strptime(last_modified_date, "%Y-%m-%dT%H:%M:%S")
                    print("last modified:" + str(last_modified_date))

                    currdate = datetime.utcnow()
                    print("currdate:" + str(currdate))

                    difference = currdate - last_modified_date
                    one_hour = timedelta(minutes=60)

                    if(last_modified_date.date() == currdate.date()): #check that lastmodified is within an hour from current time
                        if(difference <= one_hour):
                            break
                
                time.sleep(120)
                counter += 3

            except urllib.error.HTTPError as e:
                raise Exception('HTTP Error ' + str(e.code) + ' : Request URI not found ' + str(e.read()))

        if(counter >= 300):
            sys.exit("Stopped due to timeout")

    def uploadCsv(self, dataset_id):
        """
        Upload csv file to Wave.
        :return: return False if any error happens, else return True
        """
        self.removeLocalFiles()
        access_token = self._wave_connector.get_access_token()
        successFiles = []
        
        for dataFile in os.listdir(self._dataConfig.dataFolder):
            toBeProcessedFile = self._dataConfig.dataFolder + "/" + dataFile
            
            # skip non-csv files
            if not toBeProcessedFile.endswith('.csv'):
                continue
            # skip dirs
            if os.path.isdir(toBeProcessedFile):
                continue
            try:
                self.uploadToWave(toBeProcessedFile, access_token)
            except urllib.error.URLError as e:
                JsonUtils.pretty_print(str(e.read()))
                raise Exception('HTTP Error %s: -- see error: %s' %(e.code, str(e.read())))

            if self._setup.is_verify == 'true':
                self.checkStatus(access_token, dataset_id)
            
            file = toBeProcessedFile
            file = file.split("/")
            csvFile = ""
            
            for elem in file:
                if('.csv' in elem):
                    csvFile = elem

            successFiles.append(csvFile)

        self.moveSuccessFiles(successFiles)

