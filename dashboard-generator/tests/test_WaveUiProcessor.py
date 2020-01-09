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
from ds_generator.WaveUiProcessor import WaveUiProcessor
from ds_generator.Models import Dashboard, Container

import mock
import unittest
import json
import requests
import os


class WaveUiProcessorTestSuite(unittest.TestCase):
    def setUp(self):
        self.mock_config = "tests/test.ini"
        self.mock_template_path = "tests/templates"
        self.mock_saql_path = "tests/saql"
        self.mock_environment = "sandbox"
        self.mock_download = "tests/download"
        self.mock_output = "tests/output"

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
        self.mock_container_list = [
            Container(
                name='container_1',
                display_name='Container 1',
                template_file='container_widget.json',
                colspan=1,
                col=2,
                row=2,
                rowspan=4
            ),
            Container(
                name='container_2',
                display_name='Container 2',
                template_file='container_widget.json',
                colspan=2,
                col=0,
                row=5,
                rowspan=4
            ),
            Container(
                name='container_3',
                display_name='Container 3',
                template_file='container_widget.json',
                colspan=5,
                col=4,
                row=20,
                rowspan=2
            )
        ]

        self.single_dashboard = Dashboard(
            wave_id='0FK0u00000000gDGAQ',
            dashboard_name='horizon_analytics_1',
            dashboard_type='dashboard_type',
            display_name='Horizon Analytics 1',
            url='/services/data/v46.0/wave/dashboards/0FK0u00000000gDGAQ/',
            link_var='link_var',
            group_name='group_name',
            folder_id='00l0u000000Dn3CAAS',
            env='sandbox'
        )

        self.mock_wave_id = '0FK0u00000000gDGAQ'
        self.mock_json_response = ' { "url": "/services/data/v46.0/wave/dashboards/0FK0u00000000fyGAA",' \
                                  '"id": "0FK0u00000000fyGAA",'\
                                  '"name": "sample_dashboard",' \
                                  '"folder": { "id": "00l0u000000Dn3CAAS" } }'
        self.mock_json = json.dumps(
            "{ 'json': 'json_content' }"
        )

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_delete_dashboard_list(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                                   mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_wave_connector_in_processor.delete_dashboard_by_id.return_value.status_code = 204
        mock_entity_service_in_processor.get_dashboard_containers.return_value = self.mock_container_list

        self.wave_ui_processor.delete_dashboard_list(self.mock_dashboard_list)
        self.assertEquals(self.wave_ui_processor.conn.delete_dashboard_by_id.return_value.status_code, 204)

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_upload_single_dashboard(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                                     mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_wave_connector_in_processor.create_dashboard.return_value = json.loads(self.mock_json_response)  # 201
        mock_entity_service_in_processor.get_dashboard_by_id.return_value = self.single_dashboard
        mock_entity_service_in_processor.get_dashboard_containers.return_value = self.mock_container_list

        self.wave_ui_processor.upload_single_dashboard(self.mock_json, self.mock_wave_id)

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_create_dashboards(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                               mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_ui_mgr_in_processor.get_dashboards.return_value = self.mock_dashboard_list
        mock_ui_mgr_in_processor.generate_json.return_value = self.mock_json
        with mock.patch('ds_generator.WaveUiProcessor.WaveConnector.session.patch') as mock_update:
            with mock.patch('ds_generator.WaveUiProcessor.check_response') as mock_check_response:
                # dashboard does exist
                mock_update.return_value.status_code = 200
                self.wave_ui_processor.create_dashboards()

                # dashboard does not exist in Wave
                mock_check_response.side_effect = requests.exceptions.RequestException
                self.wave_ui_processor.create_dashboards()

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_update_dashboards(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                               mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_ui_mgr_in_processor.get_dashboards.return_value = self.mock_dashboard_list
        mock_ui_mgr_in_processor.generate_json.return_value = self.mock_json
        mock_wave_connector_in_processor.update_dashboard_by_id.return_value = 200

        self.wave_ui_processor.update_dashboards()

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_delete_dashboards(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                               mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_ui_mgr_in_processor.get_dashboards.return_value = self.mock_dashboard_list

        # no passed name
        self.wave_ui_processor.delete_dashboards()
        # passed name
        self.wave_ui_processor.delete_dashboards("horizon_analytics_1")

    @mock.patch('ds_generator.WaveUiProcessor.WaveConnector')
    @mock.patch('ds_generator.WaveUiProcessor.EntityService')
    @mock.patch('ds_generator.WaveUiProcessor.UiManager')
    def test_download_dashboards(self, mock_wave_connector_in_processor, mock_entity_service_in_processor,
                                 mock_ui_mgr_in_processor):
        # create a wave_ui_processor instance
        self.wave_ui_processor = WaveUiProcessor(self.mock_config)
        self.wave_ui_processor._entity_service = mock_entity_service_in_processor
        self.wave_ui_processor.conn = mock_wave_connector_in_processor
        self.wave_ui_processor._ui_mgr = mock_ui_mgr_in_processor

        mock_ui_mgr_in_processor.get_dashboards.return_value = self.mock_dashboard_list
        with mock.patch('ds_generator.WaveUiProcessor.read_file') as mock_read_file:
            self.wave_ui_processor.download_dashboards()
            self.assertTrue(os.path.exists(self.mock_download + "/" + self.mock_environment))

            # clear previous files
            dirs = os.listdir(self.mock_download + "/" + self.mock_environment)
            for prev_files in dirs:
                os.remove(self.mock_download + "/" + self.mock_environment + "/" + prev_files)

            self.wave_ui_processor.download_dashboards()
            self.assertEquals(len(os.listdir(self.mock_download + "/" + self.mock_environment)), 2)
            # removing files in mock_download
            for root, dirs, files in os.walk(self.mock_download, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
