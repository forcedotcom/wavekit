"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# -*- coding: utf-8 -*-

import unittest
import mock
from mock import patch
import os
import ConfigParser
from wave_common.config import LoginInfo
from wave_uploader.config import DataConfig, Setup
from wave_uploader.wave_uploader import WaveUploader
from wave_common.utils import get_current_file_path, save_file, create_dirs, remove_dirs


class WaveUploaderTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.RawConfigParser()
        config.read(get_current_file_path(__file__) + "/../tests/test.ini")
        self._producer_name = "testProducer"
        self._dataset = "testDataSet"
        self._mode = "Overwrite"
        self._loginInfo = LoginInfo('wave-login', config)
        self._dataConfig = DataConfig(
            get_current_file_path(__file__),
            "../test-data",
            self._producer_name)
        self._setup = Setup(config)

        self._testUploader = WaveUploader(
            self._loginInfo,
            self._dataset,
            self._mode,
            self._dataConfig,
            self._setup)
        create_dirs(self._dataConfig.doneFolder)
        create_dirs(self._dataConfig.dataFolder)
        create_dirs(self._dataConfig.errorFolder)

    def tearDown(self):
        remove_dirs(self._dataConfig.doneFolder)
        remove_dirs(self._dataConfig.dataFolder)
        remove_dirs(self._dataConfig.errorFolder)

    def createTestCsv(self, folder, filename):
        # print "Filename:" + filename
        save_file(folder + "/" + filename, "header1,header2\nl11,l12\nl21,l22")

    def testUploadSuccess(self):
        # no error
        with patch.object(self._testUploader, '_runCommand', return_value=0) as patch_shell:
            self.createTestCsv(self._dataConfig.dataFolder, 'test.csv')
            self._testUploader.uploadCsv()
            self.assertTrue(os.listdir(self._dataConfig.dataFolder) == [])
            self.assertTrue(len(os.listdir(self._dataConfig.doneFolder)) == 1)

    def testUploadFailure(self):
        # error to upload
        with patch.object(self._testUploader, '_runCommand', return_value=1) as patch_shell:
            self.createTestCsv(self._dataConfig.dataFolder, 'test.csv')
            self._testUploader.uploadCsv()
            self.assertTrue(os.listdir(self._dataConfig.dataFolder) == [])
            self.assertTrue(len(os.listdir(self._dataConfig.errorFolder)) == 1)

    if __name__ == '__main__':
        unittest.main()
