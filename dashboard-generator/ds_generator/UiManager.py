"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from .orm.EntityService import EntityService
from .WaveUiServices import WaveUIServices
from wave_common.utils import read_file, save_file

class UiManager:
    def __init__(self, db_config, output, template_path, saql_path, download, environment):
        self._db_conf = db_config
        self._entity_service = EntityService(self._db_conf)
        self.output = output
        self.template_path = template_path
        self.saql_path = saql_path
        self.download = download
        self.environment = environment

        self._wave_ui_service = WaveUIServices(self._db_conf, self.output, self.template_path, self.saql_path, self.environment)

    def get_dashboards(self, env):
        """
        Method returns all Dashboards in the provided environment
        :param env:
        :return dashboards:
        """
        return self._entity_service.get_dashboards_by_env(env)

    def generate_json(self, ds_name, dashboard_env):
        """
        Method uses string replacement to insert datasets into JSON of the provided Dashboard
        :param dashboard_id:
        :param dashboard_env:
        :return:
        """
        template_name = self._wave_ui_service.execute(ds_name)
        dashboard_name = self._entity_service.get_dashboard_by_name(ds_name).display_name

        datasets = self._entity_service.get_datasets_by_env(dashboard_env)
        data = {}
        for ds in datasets:
            data[ds.type] = ds.name

        dashboard = read_file(template_name)
        for key, value in data.items():
            dashboard = dashboard.replace("%(" + key + ")s", value)

        with open(self.output + '/' + dashboard_name + '_dashboard.json', 'w') as fout:
            fout.write(str(dashboard))
        return dashboard


    def save_dashboard(self, dashboard):
        """
        save changed dashboard
        :param dashboard: dashboard object
        :return:
        """
        self._entity_service.save_dashboard(dashboard)