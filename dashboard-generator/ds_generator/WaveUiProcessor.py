#!/usr/local/bin/python

# -*- coding: utf-8 -*-
""" Wave Ui Generator processor
Usage:
  WaveUiProcessor.py (<conf_file>) (--create | --update | --download)
  WaveUiProcessor.py (<conf_file>) (--delete) [<dashboard_name>]
  WaveUiProcessor.py (-h | --help)

Options:
  conf_file       config file name
  -h --help       Show this screen.
"""


"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from docopt import docopt
from configparser import ConfigParser
from wave_common.wave_connector import WaveConnector
from wave_common.config import LoginInfo
from wave_common.utils import read_file, save_file, Logger, check_response
from .config import DashboardInfo, DatabaseConfig
from .UiManager import UiManager
from datetime import datetime
import json
import requests
from wave_common.JsonUtils import pretty_print, load_json_from

from .orm.EntityService import EntityService
from .Models import Dashboard

logger = Logger.logger


class WaveUiProcessor:

    def __init__(self, config_file):
        parser = ConfigParser()
        parser.optionxform=str
        config_file = config_file
        Logger.logger.info(config_file)
        parser.read(config_file)
        database_conf = DatabaseConfig(parser)

        self._db_conf = database_conf
        self.template_path = parser.get("Paths", 'template_path')
        self.saql_path = parser.get("Paths", 'saql_path')
        self.environment = parser.get('Wave_Config', 'environment')
        download = parser.get('Paths', 'download')
        output = parser.get('Paths', 'output')
        self.download = download + "/" + self.environment
        self.output = output + "/" + self.environment
        
        # login and config
        self.login_config = LoginInfo('login', parser)
        self.wave_config = DashboardInfo(parser)
        self._ui_mgr = UiManager(self._db_conf, self.output, self.template_path, self.saql_path, self.download,
                                 self.environment)
        self._entity_service = EntityService(self._db_conf)
        self.conn = WaveConnector(self.login_config, self.wave_config.authUrl, self.wave_config.resource_url)
        self.conn.login()

    def delete_dashboard_list(self, dashboard_list):
        """
        Method removes all dashboards in provided list and associated dashboard-page from database
        :param dashboard_list:
        :return:
        """
        for d in dashboard_list:
            logger.info("Deleting dashboard %s (%s)" % (d.display_name, d.wave_id))
            response = self.conn.delete_dashboard_by_id(d.wave_id)
            logger.info(response)

            logger.info("Removing dashboard %s (%s) from database" % (d.display_name, d.wave_id))
            containers = self._entity_service.get_dashboard_pages(d.wave_id)
            for c in containers:
                self._entity_service.delete_relationship_by_id(d.wave_id, c.name)
            self._entity_service.delete_dashboard_by_id(d.wave_id)
            logger.info("Removed from database!")

    def upload_single_dashboard(self, json_content, prev_wave_id):
        """
        Method uploads dashboard to Wave and updates dashboard with valid Wave ID in database
        :param json_content:
        :param prev_wave_id:
        :return:
        """
        response = self.conn.create_dashboard(json.loads(json_content))

        new_wave_id = response["id"]
        url = response["url"]
        folder_id = response["folder"]["id"]

        logger.info("Dashboard %s (%s) created successfully" % (response["name"], new_wave_id))
        # get info from original wave_id
        db_dashboard = self._entity_service.get_dashboard_by_id(prev_wave_id)

        # add new dashboard to DB
        self._entity_service.add_new_dashboard(
            Dashboard(new_wave_id, db_dashboard.dashboard_name, db_dashboard.dashboard_type, db_dashboard.display_name,
                      url, db_dashboard.link_var, db_dashboard.group_name, folder_id, self.environment)
        )

        db_pages = self._entity_service.get_dashboard_pages(prev_wave_id)

        # update all the relationships
        for c in db_pages:
            self._entity_service.add_relationship(new_wave_id, c.name)
            self._entity_service.delete_relationship_by_id(prev_wave_id, c.name)

        self._entity_service.delete_dashboard_by_id(prev_wave_id)
        logger.info("Updated database")

    def create_dashboards(self):
        """
        Method uploads new dashboard to Wave if it does not exist and updates existing dashboard otherwise
        :return:
        """
        dashboards = self._ui_mgr.get_dashboards(self.environment)
        for ds in dashboards:
            json_content = self._ui_mgr.generate_json(ds.dashboard_name, ds.env)
            try:
                # adding to existing dashboard (valid wave_id)
                # create_input_object = {'folder': ds.folder_id, 'name': ds.dashboard_name, 'description': ds.display_name, 'state': json.loads(json_content)}
                # pretty_print(load_json_from(json_content))
                response_ds = self.conn.create_dashboard(data=load_json_from(json_content))
                pretty_print(response_ds, 1)
                logger.info("Dashboard %s (%s) updated ID %s" % (ds.display_name, ds.dashboard_name, response_ds['id']))
                ds.wave_id = response_ds['id']
                ds.url = response_ds['url']
                self._ui_mgr.save_dashboard(ds)
            except requests.exceptions.RequestException:
                # Wave ID from dashboard in DB does not exist
                logger.info("Creating dashboard")
                # self.upload_single_dashboard(json_content, ds.wave_id)
                logger.info("<Response [201]>")

    def update_dashboards(self):
        """
        Method updates existing dashboards with generated JSON from metadata
        :return:
        """
        dashboards = self._ui_mgr.get_dashboards(self.environment)
        for d in dashboards:
            json_test = self._ui_mgr.generate_json(d.dashboard_name, d.env)
            response = self.conn.update_dashboard_by_id(d.wave_id, json.loads(json_test))
            logger.info(response)
            logger.info("Dashboard %s (%s) updated" % (d.display_name, d.wave_id))

    def delete_dashboards(self, dashboard_name=""):
        """
        Method deletes dashboard by its name if provided or all dashboards otherwise
        :param dashboard_name:
        :return:
        """
        dashboards = self._ui_mgr.get_dashboards(self.environment)
        if dashboard_name:
            dashboards = filter(lambda x: x.get_dashboard_name() == dashboard_name, dashboards)
            self.delete_dashboard_list(dashboards)
        else:
            self.delete_dashboard_list(dashboards)

    def download_dashboards(self):
        """
        Method saves JSON file of all dashboards that were uploaded/updated in the same session
        :return:
        """
        today = datetime.now()
        dashboards = self._ui_mgr.get_dashboards(self.environment)
        for d in dashboards:
            file_name = self.output + "/" + d.display_name + "_dashboard.json"
            content = read_file(file_name)
            download_path = self.download + "/" + d.display_name + "_" + d.env + "_" + today.strftime('%Y%m%d%H%M') + "_dashboard.json"
            save_file(download_path, content)
            logger.info("Dashboard %s (%s) saved successfully" % (d.display_name, d.wave_id))


def main(arguments):
    if arguments['<conf_file>']:
        config_file = arguments['<conf_file>']
        ui_processor = WaveUiProcessor(config_file)
        if arguments['--create']:
            ui_processor.create_dashboards()
        if arguments['--update']:
            ui_processor.update_dashboards()
        if arguments['--delete']:
            ui_processor.delete_dashboards(arguments['<dashboard_name>'])
        if arguments['--download']:
            ui_processor.download_dashboards()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if(arguments):
        main(arguments)
    else:
        Logger.logger.error(error)



