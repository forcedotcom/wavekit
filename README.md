# Wave Kit

Developed within Salesforce, Wavekit is a a python3-based library to upload csv and create Salesforce Analytics dashboards. Designed with injection and customization in mind, these libraries are flexible and easy for any developer with some python knowledge to adopt and customize. 

Our scripts have been tested on postgres databases. If you are on working on a different database, you may need to enhance the sql script or datamodel to make it work. 

This folder includes sample data, wave_common, wave-uploader and dashboard-generator.
 
* Sample data contains script to generate a test database, and a set of sample data to populate sample table 
* Wave_common contains reusable functions for login, reformatting, logging etc. Using the common login function from wave_common module.
* Wave uploader provides functions to split CSV data into chunks to upload into Wave either in overwriting mode or appending mode. It also has a feature to validate uploads. 
* Dashboard generator has scripts to generate metadata models, populate sample metadata, sample JSON templates and SAQL queries to generate a dashboard.

## Configurations
Under conf folder of both wave-uploader and dashboard-generator, a sample sandbox.ini file is provided. During implementation, you should set another ini file for production purpose. 

In those configurations, the endpoint for sandbox should be:
 endpoint=https://test.salesforce.com
 and for production:
 endpoint=https://www.salesforce.com or redirection URL.
 
 authUrl should be set as:
 authUrl=https://test.salesforce.com/services/oauth2/token
for sandbox. For production, the parameter should be: 
authUrl=https://www.salesforce.com/services/oauth2/token

Client Id and Client secret could be get as in instruction on:
https://developer.salesforce.com/forums/?id=906F0000000AfcgIAC


## Sample App

Our sample app provides an example of cost analytics. It has a cost data set, period data set, breakdown data set, sort order data set and sort type data set. The cost data set container some example cost data with multiple dimensions. Period data only has one date type dimension which is used for filtering. The rest of three datasets are intended for structure purpose which generates dynamic SAQL on fly. 
Our sample uploader will load all five data sets, even though the structural data set only needs to be uploaded once. 
Our sample dashboard board will produce a sample dashboard with complex filtering and dynamic SAQL byased on user selections. 
 

 

