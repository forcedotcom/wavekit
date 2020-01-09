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
from mock import Mock, patch, MagicMock
from wave_common.utils import get_current_file_path, save_file, create_dirs
from wave_uploader.wave_data_uploader import WaveDataUploader

class TestWaveDataUploader(unittest.TestCase):
    def setUp(self):
        self._dataUploader = WaveDataUploader(
            get_current_file_path(__file__) + "/../tests/test.ini", 'Overwrite')

    def tearDown(self):
        pass

    def testExecuteOneProducer(self):
        mock_wave_uploader = Mock()
        attrs = {'name.return_value': 'mock_producer'}
        mock_producer = Mock(**attrs)
        for config in self._dataUploader._producerConfigs:
            config.producer = mock_producer

        with patch.object(self._dataUploader, '_waveUploader', return_value=mock_wave_uploader) as mockMethod:
            self._dataUploader.execute()
            mock_producer.pull.assert_called_once()
            mockMethod.assert_called_once()

    def testExecuteTwoProducers(self):
        mock_wave_uploader = Mock()
        attrs = {'name.return_value': 'mock_producer'}
        mock_producer1 = Mock(**attrs)
        mock_producer2 = Mock(**attrs)
        # mock_config = MagicMock(producer=mock_producer2)

        self._dataUploader._producerConfigs = []
        self._dataUploader._producerConfigs.append(
            MagicMock(producer=mock_producer1))
        self._dataUploader._producerConfigs.append(
            MagicMock(producer=mock_producer2))

        with patch.object(self._dataUploader, '_waveUploader', return_value=mock_wave_uploader) as mock_method:
            self._dataUploader.execute()
            mock_producer1.pull.assert_called_once()
            mock_producer2.pull.assert_called_once()
            self.assertEqual(mock_wave_uploader.uploadCsv.call_count, 2)

if __name__ == '__main__':
    unittest.main()
