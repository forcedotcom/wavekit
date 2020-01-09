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
from wave_core_ui.config import DBConfig
from wave_core_ui.db_connector import DatabaseConnector
from datetime import datetime, timedelta
import random

class DataSimulator(object):
    metric_array = ['core', 'data_dot_com', 'desk_dot_com', 'heroku', 'pardot', 'sfiq']
    db_config = DBConfig('localhost', 'pulse', 'postgres', 'TODO', 5)

    def __init__(self):
        self._db_connector = DatabaseConnector(self.db_config)

    def _random_avail(self):
        total_avail = 40552
        perc = 0.99 + (0.1*(0.5 - random.random()) )
        return [round(total_avail*perc, 0), perc]

    def _random_other_metric(self):
        base_minutes = 400
        perc = 0.5 + (0.1*(0.5 - random.random()) )
        return [round(base_minutes*perc, 0), perc]

    def _random_latency(self):
        return random.randint(0,100)

    def _random_MoM_QoQ(self):
        return random.randint(0, 10)/100.0

    def get_fiscal_year_quarter(self, date):
        month = date.month
        year = date.year
        if month == 1:
            year = year - 1
            quarter = 4
        elif month >= 2  and month < 5:
            quarter = 1
        elif month >= 5 and month < 8:
            quarter = 2
        elif month >= 8 and month < 11:
            quarter = 3
        else:
            quarter = 4
        return [year, quarter]

    def insertRow(self, property, product, fiscal_year, fiscal_quarter, fiscal_month, time_agg_level, region_agg_level, env_agg_level, instance_agg_level, available_data_minutes, total_available_minutes, total_planned_downtime_minutes,  total_unplanned_downtime_minutes, degraded_available_minutes, availability_perc, planned_downtime_perc, unplanned_downtime_perc,  degraded_available_perc, latency, last_modified_date):
        sql = 'insert into pulse.pulse_daily_agg( property, product_line, fiscal_year, fiscal_quarter, fiscal_month, time_agg_level, region_agg_level, env_agg_level, instance_agg_level, available_data_minutes, total_available_minutes, total_planned_downtime_minutes, total_unplanned_downtime_minutes, degraded_availability_minutes, availability_perc,  planned_downtime_perc,  unplanned_downtime_perc, ' \
        + ' degraded_availability_perc, latency, last_modified_date) ' \
        + ' values( \'{property}\', \'{product}\' , ' \
        + ' \'{fiscal_year}\', \'{fiscal_quarter}\', \'{fiscal_month}\', ' \
        + ' \'{time_agg_level}\', \'{region}\', \'{env}\', \'{instance}\', {data_minutes}, {avail_min}, {planned_min}, {unplanned_min}, {degraded_min}, ' \
        + ' {avail_perc},  {planned_perc},' \
        + ' {unplanned_perc},  {degraded_perc}, {latency}, \'{last_modified}\' ) '
        vars = {'property':property, 'product':product,
        'fiscal_year':fiscal_year, 'fiscal_quarter':fiscal_quarter, 'fiscal_month':fiscal_month, 'time_agg_level':time_agg_level,
        'region':region_agg_level, 'env':env_agg_level, 'instance':instance_agg_level,
        'data_minutes':available_data_minutes, 'avail_min':total_available_minutes,
        'avail_perc':availability_perc, 'planned_min':total_planned_downtime_minutes, 'unplanned_min':total_unplanned_downtime_minutes, 'degraded_min': degraded_available_minutes,
        'avail_perc':availability_perc, 'planned_perc':planned_downtime_perc,
        'unplanned_perc':unplanned_downtime_perc, 'degraded_perc':degraded_available_perc,
        'degraded_perc':degraded_available_perc, 'latency':latency, 'last_modified':last_modified_date.strftime('%Y-%m-%d')
        }
        exec_sql = sql.format(**vars)
        print exec_sql
        self._db_connector.execute_insertOrUpdate(exec_sql)


    def execute(self):
        self._db_connector.execute_insertOrUpdate('delete from pulse.pulse_daily_agg cascade;')

        for property in self.metric_array:
            date = datetime.now()

        #simulate 12 mon
            for i in range(1, 13):
                [data_minutes, _] = self._random_avail()
                [avail_min, avail_perc]  = self._random_avail()
                [unplanned_min, unplanned_perc] = self._random_other_metric()
                [planned_min, planned_perc] = self._random_other_metric()
                [degraded_min, degraded_perc] = self._random_other_metric()
                fiscal_month = date.strftime('%b').upper()
                [fiscal_year, fiscal_quarter] = self.get_fiscal_year_quarter(date)
                latency = self._random_latency()
                fiscal_year = 'FY'+str(fiscal_year)[2::]
                fiscal_quarter = 'Q' + str(fiscal_quarter)
                region = 'AMER'
                env = 'PROD'
                product = 'Test'
                date_key = date.strftime('%Y%m%d')
                format_date = date.strftime('%Y-%m-%d')
                #time agg
                #ALL-FY17,<Q>-FY17-YTD,<M>-FY17-YTD, QoQ, MoM
                for instance in ['NA7', 'ALL']:
                        #Month
                    self.insertRow( property, product, fiscal_year, fiscal_quarter, fiscal_month, 'ALL', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, avail_perc, planned_perc, unplanned_perc,  degraded_perc, latency, date)

                    if i == 1:
                        #YTD data only most recent month

                        self.insertRow(property, product, fiscal_year, fiscal_quarter, fiscal_month, fiscal_month +'-FY17-YTD', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, avail_perc, planned_perc, unplanned_perc,  degraded_perc, latency, date)

                        #MoM only recent month
                        self.insertRow( property, product, fiscal_year, fiscal_quarter, fiscal_month, 'MoM', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, self._random_MoM_QoQ(), self._random_MoM_QoQ(), self._random_MoM_QoQ(),  self._random_MoM_QoQ(), self._random_MoM_QoQ(), date)
                        #QoQ
                        self.insertRow( property, product, fiscal_year, fiscal_quarter, fiscal_month, 'QoQ', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, self._random_MoM_QoQ(), self._random_MoM_QoQ(), self._random_MoM_QoQ(),  self._random_MoM_QoQ(), self._random_MoM_QoQ(), date)
                    #Quarter data
                    if (i % 3) == 0:
                            self.insertRow( property, product, fiscal_year, fiscal_quarter, 'ALL', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, self._random_MoM_QoQ(), self._random_MoM_QoQ(), self._random_MoM_QoQ(),  self._random_MoM_QoQ(), self._random_MoM_QoQ(), date)
                            #quarter YTD
                            self.insertRow(property, product, fiscal_year, fiscal_quarter, fiscal_month, fiscal_quarter + '-FY17-YTD', region, env, instance, data_minutes, avail_min, planned_min,  unplanned_min, degraded_min, avail_perc, planned_perc, unplanned_perc,  degraded_perc, latency, date)
                date = date - timedelta(days=31)

        self._db_connector.commitAndClose()
if __name__ == '__main__':
    simulator = DataSimulator()
    simulator.execute()
