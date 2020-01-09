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
from wave_common.db_connector import DatabaseConnector

import mock
import unittest
from pgdb import Error

class DbConnectorTestSuite(unittest.TestCase):
    def setUp(self):
        self.mock_database_config = mock.Mock(hostname="hostname",
                                                 database="database",
                                                 username="username",
                                                 password="password",
                                                 timeout=5)

    @mock.patch('wave_common.db_connector.connect')
    def test_login(self, mock_connect):
        # login succeed
        db_connector = DatabaseConnector(self.mock_database_config)
        mock_connect.return_value = mock.Mock(status="success")
        conn = db_connector._connect()
        self.assertIsNotNone(conn)
        self.assertEqual(conn.status, "success")

        # login failed
        db_connector = DatabaseConnector(self.mock_database_config)
        with self.assertRaises(SystemExit) as cm:
            mock_connect.return_value = mock.Mock(status="failure")
            mock_connect.side_effect = Exception("mock exception")
            conn = db_connector._connect()
            self.assertIsNotNone(conn)
            self.assertEqual(conn.status, "failure")
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.db_connector.connect')
    def test_get_cur(self, mock_connect):
        db_connector = DatabaseConnector(self.mock_database_config)
        mock_connect.return_value = mock.Mock(status="success")
        self.assertIsNotNone(DatabaseConnector.get_cursor(db_connector))

    @mock.patch('wave_common.db_connector.connect')
    def test_execute_query(self, mock_connect):

        #connecting to database
        mock_connect.return_value = mock.Mock(status="success")
        mock_cursor = mock.Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [("row1col1", "row1col2", "row1col3"),
                                              ("row2col1", "row2col2", "row3col3")]
        mock_cursor.description = []
        db_connector = DatabaseConnector(self.mock_database_config)

        result = db_connector.execute_query("fake-query-success")
        #executing query successfully
        self.assertEqual(result, ([("row1col1", "row1col2", "row1col3"),
                                  ("row2col1", "row2col2", "row3col3")], []))


        #executing query with failure
        with self.assertRaises(SystemExit) as cm:
            mock_cursor.execute.side_effect = Error("mock exception")
            mock_cursor.fetchall.return_value = None
            db_connector = DatabaseConnector(self.mock_database_config)
            db_connector.execute_query("fake-query-failure")
        self.assertEqual(cm.exception.code, 1)

        #executing connection failure
        mock_connect.return_value = None
        db_connector = DatabaseConnector(self.mock_database_config)
        db_connector.execute_query("fake-query-failure")

    @mock.patch('wave_common.db_connector.connect')
    def test_execute_insertOrUpdate(self, mock_connect):
        #connecting to database
        mock_connect.return_value = mock.Mock(status="success")
        mock_cursor = mock.Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        db_connector = DatabaseConnector(self.mock_database_config)

        result = db_connector.execute_insertOrUpdate("fake-query-success")
        #executing query successfully
        self.assertEqual(result, None)

        #executing query with failure
        with self.assertRaises(SystemExit) as cm:
            mock_cursor.execute.side_effect = Error("mock exception")
            db_connector = DatabaseConnector(self.mock_database_config)
            db_connector.execute_insertOrUpdate("fake-query-failure")
        self.assertEqual(cm.exception.code, 1)
        #
        # #executing connection failure
        mock_connect.return_value = None
        db_connector = DatabaseConnector(self.mock_database_config)
        db_connector.execute_insertOrUpdate("fake-query-failure")

if __name__ == '__main__':
    unittest.main()
