# Copyright (c) 2018, Salesforce.com, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# * Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""

wave data uploader

Usage:
  wave_uploader/uploader.py (<config_file>) (--append | --overwrite)
  wave_uploader/uploader.py (-h | --help)

Options:
  config_file       config file
  --append         append data in wave
  --overwrite      overwrite wave data
  -h --help         Show this screen.
"""
from docopt import docopt
from configparser import ConfigParser
import subprocess

from wave_common.utils import exception_handler
from wave_common.core_logger import Logger
from wave_common.config import LoginInfo
from wave_common.wave_connector import WaveConnector
from uploader_config import Setup, ProducerConfig
from data_uploader import WaveUploader


class WaveDataUploader:
    """
    This class is used to create a wave dataset uploader object by given config file location.
    """

    def __init__(self, configFile, mode):
        """
        Constructor for wave data uploader.
        :param configFile: config file name
        """
        self._uploadMode = mode
        self._config = ConfigParser()
        self._config.read(configFile)

        self._setup = Setup(self._config)
        self._loginInfo = LoginInfo('wave-login', self._config)

        self._wave_connector = WaveConnector(self._loginInfo, self._setup.auth_url, self._setup.resource_url)

        self._producerConfigs = []
        for name in self._setup.producers:
            producerConfig = ProducerConfig(
                name.strip(), self._config, self._setup.rootPath, self._setup.dataFolder)
            self._producerConfigs.append(producerConfig)

    def _waveUploader(self, loginInfo, dataset_id,  dataset, uploadMode, dataConfig, setup):
        """
        this method is a stub methd for tests
        """
        return WaveUploader(loginInfo, dataset_id, dataset, uploadMode, dataConfig, setup)

    def execute(self):
        """
        Execute the Health Service Upload by given an starting timestamp with int type
        :return: True for running success, False for failure
        """
        try:
            self._wave_connector.login()
            for producerConfig in self._producerConfigs:
                producer = producerConfig.producer
                print(type(producer))
                subprocess.call(
                        '/bin/rm -rf ' + producerConfig.dataConfig.dataFolder + "/*.csv", shell=True)
                Logger.logger.info('pull from ' + producer.name())
                producer.pull(producerConfig.dataConfig.dataFolder)
                Logger.logger.info('upload dataset ' + producerConfig.dataset)
                waveUploader = self._waveUploader(
                    self._wave_connector,
                    producerConfig.data_id,
                    producerConfig.dataset,
                    self._uploadMode,
                    producerConfig.dataConfig,
                    self._setup)
                waveUploader.uploadCsv(producerConfig.data_id)
            return True
        except Exception as e:
            print(e)
            info = "Error while executing."
            exception_handler(info, e)
            return False


def main(arguments):
    if arguments:
        if arguments['--overwrite']:
            uploader = WaveDataUploader(arguments['<config_file>'], 'Overwrite')
        else:
            uploader = WaveDataUploader(arguments['<config_file>'], 'Append')
        uploader.execute()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
