"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import requests
import json

class DBConfig:
    """
    User defined database configuration info.
    """
    def __init__(self, hostname, database, username, password, timeout, sslmode):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.timeout = timeout
        self.sslmode = sslmode

def create_db_config_from_config(config, section_name):
    if(config.has_option(section_name, 'password_mode') and  config.get(section_name, 'password_mode') == 'local'):
        password = config.get(section_name, 'password')
    else:
        proxies = { "http": None,"https": None,} 
        request_url = config.get(section_name, 'subscriber') + '/horizon/ss/vault/' + config.get(section_name, 'vault_name') +'/secret/' + config.get(section_name, 'username')

        req = requests.get(request_url, proxies=proxies)
        res = json.loads(req.text)
        password = ""
    
        if('password' in res):
            password = res['password']
        else:
            raise Exception('Something went wrong with authentication -- see error:' + req.text)

    return DBConfig(config.get(section_name, 'hostname'), config.get(section_name, 'database'), config.get(section_name, 'username'), password, config.get(section_name, 'timeout'), config.get(section_name, 'sslmode'))
