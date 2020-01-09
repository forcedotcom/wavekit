"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
This producer object generate csv files by copying static csv file.
"""
from wave_common.db_connector import DatabaseConnector
from wave_uploader.wave_data_producer import WaveDataProducer
from wave_common.utils import create_timestamp_csv, create_dirs, read_file, get_current_file_path, save_as_csv
from wave_common.core_logger import Logger

class PeriodDataProducer(WaveDataProducer):
    def __init__(self, dbConfig):
        self._logger = Logger.logger
        self.dbConfig = dbConfig
        self._db_connector = DatabaseConnector(dbConfig)
        self.headers = ["Period"]

    def name(self):
        return "PeriodDataProducer"

    def pull(self, targetFolder):
        create_dirs(targetFolder)
        file_name = create_timestamp_csv(targetFolder)
        self._logger.info('create file:' + file_name)

        query = read_file(get_current_file_path(__file__) + "/period.sql")
        self._logger.info('the query is: ' + query)
        [rows, _] = self._db_connector.execute_query(query)
        save_as_csv(file_name, self.headers, rows)