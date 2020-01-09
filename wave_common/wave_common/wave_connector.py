"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import urllib

import requests
from .utils import check_response, exception_handler, Logger
from .core_logger import Logger
import json


"""
This module provides the connector and multiple methods with Wave Analytics.
"""
class WaveConnector(object):

    def __init__(self, login_config, auth_url, resource_url):
        """
        :param login_config: login config object
        :param dashboard_config: dashboard config object
        """
        self._logger = Logger.logger
        self.login_config = login_config
        self._auth_url = auth_url
        self._resource_url = resource_url
        self._api_url = ""
        self._session = requests.Session()
        self._access_token = None

    def login(self):
        """
        This method is used to login in the wave analytics with user info.
        :return:
        """
        self._logger.info("Login in Wave to get token")
        payload = {'client_id': self.login_config.clientID,
                   'client_secret': self.login_config.clientSecret,
                   'grant_type': self.login_config.grantType,
                   'username': self.login_config.username,
                   'password': self.login_config.password
                   }
        try:
            r = requests.post(self._auth_url, data=payload)
            print(r)
            check_response(r)
            token = r.json()["access_token"]
            self._api_url = r.json()["instance_url"]
            token_type = r.json()["token_type"]
            self._session.headers.update({'Authorization': token_type + " " + token})
            self._logger.info("Login Successfully!")
            self._access_token = token
        except requests.exceptions.RequestException as e:
            exception_handler("login error", e)

    def get_access_token(self):
        return self._access_token

    def get_api_url(self):
        return self._api_url

    def _request_url(self):
        return self.get_api_url() + self._resource_url

    def _request_external_data_url(self):
            return self._request_url() + "/sobjects/InsightsExternalData/"

    def fetch_data_by_url(self, url):
        """
        :param url: url link with type str
        :return: type dic
        """
        try:
            r = self._session.get(self._api_url + url)
            check_response(r)
            return r.json()
        except requests.exceptions.RequestException as e:
            exception_handler("fetch url error", e)

    def fetch_dashboard_by_id(self, dashboard_id):
        """
        Fetch the content of a dashboard by id.
        :param dashboard_id: type str
        :return: type dic
        """
        try:
            r = self._session.get(self._api_url + self._resource_url + "/dashboards/" + dashboard_id)
            check_response(r)
            return r.json()
        except requests.exceptions.RequestException as e:
            exception_handler("fetch id error", e)

    def create_dashboard(self, data):
        """
        Create new dashboard with json content.
        :param data: type dic, json content
        :return: type dic
        """
        try:
            r = self._session.post(self._api_url + self._resource_url + "/dashboards", json=data)
            check_response(r)
            return r.json()
        except requests.exceptions.RequestException as e:
            exception_handler("create error", e)

    def update_dashboard_by_id(self, dashboard_id, data):
        """
        Update the dashboard content with json content.
        :param dashboard_id: type str
        :param data: type dic
        :return: status code
        """
        try:
            r = self._session.patch(self._api_url + self._resource_url + "/dashboards/" + dashboard_id, json=data)
            check_response(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            exception_handler("update error", e)

    def delete_dashboard_by_id(self, dashboard_id):
        """
        Delete the dashboard by id
        :param dashboard_id: type str
        :return: status code
        """
        try:
            r = self._session.delete(self._api_url + self._resource_url + "/dashboards/" + dashboard_id)
            check_response(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            exception_handler("delete error", e)

    def fetch_data_by_name(self, category, name):
        """
        Get the json content by category and name
        :param category: type str, eg: "dashboards" or "folder"
        :param name: type str
        :return: type dic
        """
        try:
            raw_data = self.fetch_data_by_url(self._resource_url + "/" + category)
            data_list = raw_data[category]
            for data in data_list:
                if data["label"] == name:
                    return data
        except requests.exceptions.RequestException as e:
            exception_handler("fetch error", e)

    def fetch_data_by_category(self, category):
        """
        Get the json content by category
        :param category: type str, eg: "dashboards" or "folder"
        :return: type dic
        """
        try:
            raw_data = self.fetch_data_by_url(self._resource_url + "/" + category)
            return raw_data
        except requests.exceptions.RequestException as e:
            exception_handler("fetch category error", e)

    def fetch_data_by_id(self, category, data_id):
        """
        Fetch the content of a given data category by id.
        :param category: type str
        :param data_id: type str
        :return: type dic
        """
        try:
            r = self._session.get(self._api_url + self._resource_url + "/" + category + "/" + data_id)
            check_response(r)
            return r.json()
        except requests.exceptions.RequestException as e:
            exception_handler("fetch data by id error", e)

    def postInsightsExternalData(self, json_obj):
            try:
                print(self._request_external_data_url())
                response = self._session.post(self._request_external_data_url(), json=json_obj)
                insight_object_parent_id = ""
                content = response.content
                # print(str(content))
                insight_object_response = json.loads(content)
                if('id' in insight_object_response):
                    insight_object_parent_id = insight_object_response['id']
                else:
                    raise Exception('Something went wrong with creating the InsightsExternalData object -- see error: %s' % str(content))
                return insight_object_parent_id
            except urllib.error.HTTPError as e:
                err_msg = str(e.read())
                print("Fail to access Insight External Data", e.code, err_msg, sep='\t')
                raise Exception('' + str(e.code) + " " + err_msg)
