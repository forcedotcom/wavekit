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

from wave_common.wave_connector import WaveConnector

import mock
import requests
import unittest
import sys
sys.path.append("../wave_common")

class WaveConnectorTestSuite(unittest.TestCase):
    """Utils test cases."""

    def setUp(self):
        self.wave_connector = None
        self.mock_login_config = mock.Mock(clientID="fake_clientID", clientSecret="fake_clientSecret",
                                           grantType="fake_grantType", username="fake_username",
                                           password="password")
        self.mock_dashboard_config = mock.Mock(resource_url="fake_resource_url")

    @mock.patch('wave_common.wave_connector.requests.post')
    def test_login(self, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        http_error = requests.exceptions.RequestException
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        mock_post.return_value.raise_for_status.side_effect = http_error

        # login succeed
        wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")
        wave_connector.login()
        self.assertEqual(0, mock_post.raise_for_status.call_count)

        # login failed
        mock_post.return_value.status_code = 404
        with self.assertRaises(SystemExit) as cm:
            wave_connector = WaveConnector(self.mock_login_config," http://test.com", "/resource")
            wave_connector.login()
            self.assertEqual(1, mock_post.raise_for_status.call_count)
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.wave_connector.requests.post')
    @mock.patch('wave_common.wave_connector.requests.Session.get')
    def test_fetch_data_by_url(self, mock_session, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # fetch succeed
        mock_session.return_value.status_code = 200
        mock_session.return_value.json.return_value = {"foo": "bar"}
        result = self.wave_connector.fetch_data_by_url("fake url")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"foo": "bar"})

        # fetch failed
        mock_session.return_value.status_code = 404
        mock_session.return_value.json.return_value = {"foo": "bar"}
        http_error = requests.exceptions.RequestException
        mock_session.return_value.raise_for_status.side_effect = http_error

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.fetch_data_by_url("fake url")
            self.assertEqual(1, mock_session.raise_for_status.call_count)
            self.assertEqual(0, mock_session.json.call_count)
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.wave_connector.requests.post')
    @mock.patch('wave_common.wave_connector.requests.Session.get')
    def test_fetch_dashboard_by_id(self, mock_session, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # fetch succeed
        mock_session.return_value.status_code = 200
        mock_session.return_value.json.return_value = {"foo": "bar"}
        result = self.wave_connector.fetch_dashboard_by_id("fake-dashboard-id")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"foo": "bar"})

        # fetch failed
        mock_session.return_value.status_code = 404
        mock_session.return_value.json.return_value = {"foo": "bar"}
        http_error = requests.exceptions.RequestException
        mock_session.return_value.raise_for_status.side_effect = http_error

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.fetch_dashboard_by_id("fake-dashboard-id")
            self.assertEqual(1, mock_session.raise_for_status.call_count)
            self.assertEqual(0, mock_session.json.call_count)
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.wave_connector.requests.post')
    @mock.patch('wave_common.wave_connector.requests.Session.post')
    def test_create_dashboard(self, mock_session, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # create succeed
        mock_session.return_value.status_code = 200
        mock_session.return_value.json.return_value = {"foo": "bar"}
        result = self.wave_connector.create_dashboard("fake-dashboard-data")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"foo": "bar"})

        # create failed
        mock_session.return_value.status_code = 404
        mock_session.return_value.json.return_value = {"foo": "bar"}
        http_error = requests.exceptions.RequestException
        mock_session.return_value.raise_for_status.side_effect = http_error

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.create_dashboard("fake-dashboard-data")
            self.assertEqual(1, mock_session.raise_for_status.call_count)
            self.assertEqual(0, mock_session.json.call_count)
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.wave_connector.requests.post')
    @mock.patch('wave_common.wave_connector.requests.Session.patch')
    def test_update_dashboard_by_id(self, mock_session, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # create succeed
        mock_session.return_value.status_code = 200
        result = self.wave_connector.update_dashboard_by_id("fake-id", "fake-dashboard-data")
        self.assertIsNotNone(result)
        self.assertEqual(result, 200)

        # create failed
        mock_session.return_value.status_code = 404
        http_error = requests.exceptions.RequestException
        mock_session.return_value.raise_for_status.side_effect = http_error

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.update_dashboard_by_id("fake-id", "fake-dashboard-data")
            self.assertEqual(1, mock_session.raise_for_status.call_count)
            self.assertEqual(0, mock_session.json.call_count)
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('wave_common.wave_connector.requests.post')
    @mock.patch('wave_common.wave_connector.requests.Session.delete')
    def test_delete_dashboard_by_id(self, mock_session, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # create succeed
        mock_session.return_value.status_code = 200
        result = self.wave_connector.delete_dashboard_by_id("fake-dashboard-id")
        self.assertIsNotNone(result)
        self.assertEqual(result, 200)

        # create failed
        mock_session.return_value.status_code = 404
        http_error = requests.exceptions.RequestException
        mock_session.return_value.raise_for_status.side_effect = http_error

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.delete_dashboard_by_id("fake-dashboard-id")
            self.assertEqual(1, mock_session.raise_for_status.call_count)
            self.assertEqual(0, mock_session.json.call_count)
        self.assertEqual(cm.exception.code, 1)


    @mock.patch('wave_common.wave_connector.requests.post')
    # @mock.patch('shd.wave_connector.requests.Session.get')
    def test_fetch_data_by_name(self, mock_post):
        response = {
            "access_token": "fake_token",
            "instance_url": "fake_url",
            "token_type": "fake_type"
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response
        self.wave_connector = WaveConnector(self.mock_login_config, "http://test.com", "/resource")

        # create succeed
        # mock_session.return_value.status_code = 200
        # mock_session.return_value.json.return_value = {"foo": "bar"}
        self.wave_connector.fetch_data_by_url = mock.Mock(return_value={"fake-category":
                                                ({"label": "fake-name"}, {"label2": "fake-name2"})})
        result = self.wave_connector.fetch_data_by_name("fake-category", "fake-name")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"label": "fake-name"})

        # create failed

        http_error = requests.exceptions.RequestException
        self.wave_connector.fetch_data_by_url = mock.Mock(side_effect = http_error)

        with self.assertRaises(SystemExit) as cm:
            self.wave_connector.fetch_data_by_name("fake-category", "fake-name")
        self.assertEqual(cm.exception.code, 1)

    if __name__ == '__main__':
        unittest.main()
