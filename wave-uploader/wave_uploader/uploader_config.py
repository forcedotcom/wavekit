"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from wave_common.utils import import_class, validate_config, create_dirs
from dbconfig import DBConfig, create_db_config_from_config
import sys

class ProducerConfig:
    """
    A data Producer configuration
    """

    def __init__(self, name, config, rootpath, data_folder):
        self.name = name
        package = config.get(name, 'package')
        module = config.get(name, 'module')
        classname = config.get(name, 'producer')

        self.data_id = config.get(name, 'ID', fallback=None)

        sys.path.append(package)
        # print(sys.path)
        producer_class = import_class(module + '.' + classname)
        print('load producer type    ' + module + '.' + classname)
        assert producer_class is not None
        self.dataset = config.get(name, 'dataset')
        self.database_section = config.get(name, 'database')
        self.dbConfig = create_db_config_from_config(config, self.database_section)
        self.dataConfig = DataConfig(rootpath, data_folder, self.name)
        self.producer = producer_class(self.dbConfig)
        print('load producer    ' + str(producer_class))
        assert self.producer is not None

        print(type(self.producer).__name__)
        validate_config(self.__dict__)

class DataConfig:
    """
    User defined data set configuration info.
    """
    def __init__(self, rootpath, datafolder, producername):
        self.dataFolder = rootpath + '/' + datafolder + '/' + producername + "/data"
        self.doneFolder = rootpath + '/' + datafolder + '/' + producername + '/done'
        self.errorFolder = rootpath + '/' + datafolder + '/' + producername + '/errors'
        validate_config(self.__dict__)
        create_dirs(self.dataFolder)
        create_dirs(self.doneFolder)
        create_dirs(self.errorFolder)

class Setup:
    """
    User defined environment configuration info.
    """
    def __init__(self, config):
        setupSection = "Setup"
        self.producers = config.get(setupSection, 'dataProducers').split(',')
        self.endpoint = config.get(setupSection, 'endpoint')
        self.rootPath = config.get(setupSection, 'rootPath')
        self.dataFolder = config.get(setupSection, 'dataFolder')
        self.auth_url = config.get(setupSection, 'authUrl')
        self.resource_url = config.get(setupSection, 'resourceUrl')
        self.is_verify = config.get(setupSection, 'is_verify_upload')

        validate_config(self.__dict__)
