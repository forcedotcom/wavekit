# wave_common

This is Wave related python packages. It includes logger, utils, database connector, wave connector and general configuration file.

##requirements

##Python installation download from https://www.python.org/downloads

Supports python 3

- nose==1.3.7
- requests==2.11.1
- psycopg2==2.6.2
- docopt==0.6.2
- coverage==4.0.3
- JsonWeb==0.8.2
- mock==2.0.0
- pyhive=0.3.0

##install

Run the setup script
```
make init
or
pip3 install -r requirements.txt --user
```

To install the package, 
```
make install
or
python3 setup.py install --user
```

Tips: 
- one might need sudo write access to install python libraries
- If you'd like to install at system level, you can ignore the "--user" option

