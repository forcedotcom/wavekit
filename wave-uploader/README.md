# WaveDataUploader

This wave data uploader is intended to be a generic csv data uploader for Salesforce Wave.
This uploader was written for python 3.5 + environment.

The uploader allows two modes for uploading, Overwrite or Append, which shall be passed in from argument.
The password could be either configured locally with local mode. 

Additional required packages are listed in the requirements.txt.  

This uploader allows to plug-in producers through dataProducers property in Setup in order to uploader multiple datasets into wave with one command.  The data will be saved into producer folders under dataFolder as in Setup upon success/failures.

Wave Uploader Flow Diagram: https://git.soma.salesforce.com/infra-insights/wavekit/blob/czhu-ui-change/wave-uploader/Wave%20uploader%20flow.png

## Sample configuration
Below is a sample configuration, you need to fill in wave username. password etc. 
For database configuration, you could leave as it is if you are not using any database as datasource. 

```
[wave-login]
username=****
password=****
clientID=****
clientSecret=***
grantType=password
password_mode=local

[Setup]
dataProducers={list of data producers, like testData1, separated by ,}
endpoint=https://test.salesforce.com
rootPath=.
datafolder=data
authUrl=https://test.salesforce.com/services/oauth2/token
requestUrl=https://test.salesforce.com
# true or false, verify if data upload was successful
is_verify_upload=true

[testData1]
package=.
module=sample_wave_data_producer
producer=SampleWaveDataProducer
database=testdb
dataset=wave_test_data_1
ID=****

[testdb]
hostname=****
database=****
username=****
password=****
timeout=120
password_mode=local
sslmode=require

```
## Upload data
To upload data, execute as:
```
> python3 wave_uploader/uploader.py conf/sandbox.ini --overwrite
#if append data, 
> python3 wave_uploader/uploader.py conf/sandbox.ini --append
```

## Metadata 
Sometimes when uploading data to Wave, the format of the data is changed. For example, date dimension would be become a String dimension. We included some sample under metadata folder. We expect the file names are match pattern metadata_template-{dataset-name}.json. The dataset name should be same as dataset name as in .ini file of each data producer. 

