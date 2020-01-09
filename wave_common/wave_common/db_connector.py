"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from pgdb import connect
import sys
from .utils import exception_handler
from .core_logger import Logger
from sqlalchemy.orm import sessionmaker

"""
This module provides the database connector and multiple methods with postgres.
"""
class DatabaseConnector(object):
    def __init__(self, database_config):
        self._logger = Logger.logger
        self._dbConfig = database_config
        self._conn = self._connect()

    @staticmethod
    def mkSession(engine, path):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.execute("SET search_path TO " + path)
        return session

    def _connect(self):
        """
        Create the connection with database with timeout.
        :return: database connection
        """
        try:
            self._logger.info("Connecting PGDB...")
            conn = connect(database=self._dbConfig.database,
                        host=self._dbConfig.hostname+":5432",
                        user=self._dbConfig.username,
                        password=self._dbConfig.password)

            self._logger.info("PGDB connected!")
            return conn
        except Exception as e:
            info = (
                "Unable to connect to the database:" + self._dbConfig.database + " host:" + self._dbConfig.hostname
                + " username:" + self._dbConfig.username)
            exception_handler(info, e)

    def get_cursor(self):
        """
        Return the cursor of the connection.
        :return:
        """
        return self._conn.cursor()

    def execute_query(self, sql_query):
        """
        This method is used to execute the sql query and return results.
        :param sql_query: type str
        :return: rows and header
        """
        if self._conn:
            self._logger.info("executing sql query")
            cur = self.get_cursor()
            try:
                cur.execute(sql_query)
                res = cur.fetchall()
                self._logger.info("executing done")
                return res, [col[0] for col in cur.description]
            except Exception as e:
                info = "Unable to execute the query!"
                exception_handler(info, e)
        else:
            self._logger.error("PGDB not connected!")

    def execute_insertOrUpdate(self, sql_query):
        if self._conn:
            try:
                self.get_cursor().execute(sql_query)
            except Exception as e:
                info = "Unable to execute the insert or update:" + sql_query
                exception_handler(info, e)
        else:
            self._logger.error("PGDB not connected!")

    def commit_and_close(self):
        if self._conn:
            try:
                self._conn.close()
            except Exception as e:
                info = "Unable to commit and close connection"
                exception_handler(info, e)
        else:
            self._logger.error("PGDB not connected!")
