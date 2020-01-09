"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
sys.path.append("..")
from ds_generator.UiManager import UiManager
from ds_generator.Models import Dashboard, Dataset
import mock
import unittest


class UiManagerTestSuite(unittest.TestCase):
    def setUp(self):
        # mock object

        self.mock_db_config = mock.Mock(
            environment='fake_env',
            authUrl='fake_authurl',
            resourceUrl='fake_resourceurl',
            username='fake_user',
            password='fake_password',
            host='fake_host',
            database='fake_db'
        )
        self.mock_output = "output"
        self.mock_template_path = "template"
        self.mock_saql_path = "saql"
        self.mock_download = "download"
        self.mock_environment = "sandbox"

        # mock variables
        self.mock_wave_id = "mock_wave_id_1"
        self.mock_dataset_list = [
            Dataset(
                id=1,
                type='period',
                name='period',
                env='sandbox'
            ),
            Dataset(
                id=2,
                type='breakdown',
                name='breakdown',
                env='sandbox'
            ),
            Dataset(
                id=3,
                type='cost_data',
                name='CTSFPDATA',
                env='sandbox'
            )
        ]
        self.mock_dashboard_list = [
            Dashboard(
                wave_id='0FK0u00000000gDGAQ',
                dashboard_name='horizon_analytics_1',
                dashboard_type='dashboard_type',
                display_name='Horizon Analytics 1',
                url='/services/data/v46.0/wave/dashboards/0FK0u00000000gDGAQ/',
                link_var='link_var',
                group_name='group_name',
                folder_id='00l0u000000Dn3CAAS',
                env='sandbox'
            ),
            Dashboard(
                wave_id='0FK0M000000L8zvWAC',
                dashboard_name='horizon_analytics_2',
                dashboard_type='dashboard_type',
                display_name='Horizon Analytics 2',
                url='/services/data/v46.0/wave/dashboards/0FK0M000000L9BNWA0',
                link_var='link_var',
                group_name='group_name',
                folder_id='00l0M000003Ks0EQAS',
                env='sandbox'
            )
        ]

    @mock.patch('ds_generator.UiManager.EntityService')
    @mock.patch('ds_generator.UiManager.WaveUIServices')
    def test_get_dashboards(self, mock_entity_service_in_ui_mgr, mock_wave_ui_service_in_ui_mgr):
        # create a ui_mgr instance
        self.ui_mgr = UiManager(self.mock_db_config, self.mock_output, self.mock_template_path, self.mock_saql_path,
                                self.mock_download, self.mock_environment)

        self.ui_mgr._entity_service = mock_entity_service_in_ui_mgr
        self.ui_mgr._wave_ui_service = mock_wave_ui_service_in_ui_mgr

        # testing get_dashboards()
        mock_entity_service_in_ui_mgr.get_dashboards_by_env(self.mock_environment).return_value = self.mock_dashboard_list

        self.assertEquals(self.ui_mgr.get_dashboards(self.mock_environment).return_value, self.mock_dashboard_list)

    @mock.patch('ds_generator.UiManager.EntityService')
    @mock.patch('ds_generator.UiManager.WaveUIServices')
    def test_generate_json(self, mock_entity_service_in_ui_mgr, mock_wave_ui_service_in_ui_mgr):
        # create a ui_mgr instance
        self.ui_mgr = UiManager(self.mock_db_config, self.mock_output, self.mock_template_path, self.mock_saql_path,
                                self.mock_download, self.mock_environment)

        self.ui_mgr._entity_service = mock_entity_service_in_ui_mgr
        self.ui_mgr._wave_ui_service = mock_wave_ui_service_in_ui_mgr

        # testing generate_json()
        mock_entity_service_in_ui_mgr.get_dashboard_by_id(self.mock_wave_id).display_name.return_value = "replacement"
        mock_entity_service_in_ui_mgr.get_datasets_by_env(self.mock_environment).return_value = self.mock_dataset_list
        mock_wave_ui_service_in_ui_mgr.execute(self.mock_wave_id).return_value = self.mock_template_path + "/test_replacement.json"

        with mock.patch('ds_generator.UiManager.read_file') as mock_read_file:
            with mock.patch('ds_generator.UiManager.open') as mock_open:
                mock_read_file.return_value = "%(cost_data)s" \
                                              "%(breakdown)s" \
                                              "%(period)s"

                mock_open.__enter__ = mock.Mock(return_value=(mock.Mock(), None))
                mock_open.__exit__ = mock.Mock(return_value=None)

                self.ui_mgr.generate_json(self.mock_wave_id, self.mock_environment)

