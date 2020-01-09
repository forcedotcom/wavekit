# Wave Ui Dashboard Generator

## Require:
* python > 3.4

## Install:
This directory uses the following libraries:
```
docopt==0.6.2
mock==2.0.0
JsonWeb==0.8.2
SQLAlchemy==1.1.6
Jinja2==2.10.1
nose==1.3.7
```

Required libraries are also listed in `requirements.txt` and can be installed with
```
make init
or 
pip3 install -r requirements.txt
```

In addition, this directory requires local installation of the **wave_common** repository.


## Overview

ER Diagram:
https://git.soma.salesforce.com/infra-insights/wavekit/blob/czhu-ui-change/dashboard-generator/er_diagram_cts.png

The ER Diagram describes the relationship between different UI components and how they are generated from the metadata model.


Code Structure:
https://git.soma.salesforce.com/infra-insights/wavekit/blob/czhu-ui-change/dashboard-generator/wave_diagram.jpg

## Set up metadata database

A sample config, db_env.cfg. is under conf folder. Please please customize with your database info, 
``` 
DB_HOST=""
DB_PASSWORD=""
DATABASE=""
DB_USER=""
```
After that, you can run script as 
```
bin/metadata_db.sh [prod|staging] conf/db_env.conf

```

the prod/staging environment stands for the execution environment. Typically staging refers to a Salesforce sanbdox environment, and production is a Salesforce production instance.

## Usage:
`docopt` is used to parse arguments and run the script. See below for
help info.

```
""" Wave Ui Generator processor
Usage:
  python3 ds_generator/WaveUiProcessor.py (<conf_file>) (--create | --update | --delete | --download)
  WaveUiProcessor.py (-h | --help)

Options:
  conf_file       config file name
  -h --help       Show this screen.
"""
```

Below are some examples:

## Examples:
**Load data from UI database and generate dashboards on Wave**
```
python3 ds_generator/WaveUiProcessor.py conf/sandbox.ini --create
```

**Load metadata and upload dashboards to Wave**
```
python3 ds_generator/WaveUiProcessor.py conf/sandbox.ini --update
```

**Load metadata and Download JSONs of dashboards**
```
python ds_generator/WaveUiProcessor.py conf/sandbox.ini --download
```

## Config File:
A sample ini file is listed below:
```
[login]
username={wave user}
password={wave password}
clientID={consumer id of a connected app}
clientSecret={ consumer secret of a connected app}
grantType=password
password_mode=local

[Wave_Config]
environment={sandbox or production}
authUrl={authentication URL, like https://test.salesforce.com/services/oauth2/token}
#update verion if you need
resourceUrl=/services/data/v47.0/wave

[Paths]
#below are local folder names
output=output
download=download
template_path=templates
saql_path=saql

[Database]
host={hostname}
database={database name, like testdb}
username={database user name}
password={database user password}
password_mode=local
schema={database schema, dashboard_ui_staging or dashboard_ui_production}
```

## Test:
Run all unit tests with `nose`:
```
make test
```
