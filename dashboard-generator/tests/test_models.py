"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ds_generator.Models import Property, Step, Widget, Container, Dashboard, Page
import mock
import unittest


class ModelsTestSuite(unittest.TestCase):
    def setUp(self):
        # mock config
        self.mock_db_config = mock.Mock(hostname="localhost",
                                        database="database",
                                        username="username",
                                        password="password"
                                        )

    def test_Property(self):
        property = Property(id=0, key='template_file', value='main_dashboard_infra_analytics.json')

        self.assertEquals(property.get_id(), 0)
        self.assertEquals(property.get_key(), "template_file")
        self.assertEquals(property.get_value(), "main_dashboard_infra_analytics.json")

    def test_Step(self):
        step = Step(name='step_1', display_name='Step 1', type='chart', template_file='chart_step.json')

        property = Property(id=0, key='saql_name', value='listselector_step.saql')

        step.add_property(property)

        self.assertEquals(step.get_type(), "chart")
        self.assertEquals(step.get_name(), "step_1")
        self.assertEquals(step.get_template(), 'chart_step.json')
        self.assertEquals(step.get_properties()[0].get_id(), 0)
        self.assertEquals(step.get_properties()[0].get_value(), "listselector_step.saql")

    def test_Widget(self):
        widget = Widget(name='link_3', display_name='Link 3', font_size=12, template_file='link_widget.json',
                        type='link', colspan=5, col=4, row=2, rowspan=5)

        property_1 = Property(id=0, key='dest_name', value='HorizonCostAnalyticsMoFo')

        property_2 = Property(id=1, key='dest_type', value='Dashboard')

        step = Step(name='step_1', display_name='Step 1', type='chart', template_file='chart_step.json')

        step_property = Property(id=0, key='template_file', value='main_dashboard_infra_analytics.json')

        step.add_property(step_property)

        self.assertEquals(widget.get_display_name(), "Link 3")
        self.assertEquals(widget.get_column(), 4)
        self.assertEquals(widget.get_colspan(), 5)
        self.assertEquals(widget.get_row(), 2)
        self.assertEquals(widget.get_rowspan(), 5)
        self.assertEquals(widget.get_font_size(), 12)
        self.assertEquals(widget.get_template(), "link_widget.json")
        self.assertEquals(widget.get_type(), "link")

        widget.add_properties([property_1, property_2])

        self.assertEquals(widget.get_properties()[0].get_id(), 0)
        self.assertEquals(widget.get_properties()[1].get_value(), "Dashboard")

        widget.add_step(step)

        self.assertEquals(widget.get_steps()[0].get_properties()[0].get_value(), "main_dashboard_infra_analytics.json")

    def test_Container(self):
        container = Container(name='container_33', display_name='Container 33', template_file='container_widget.json',
                              colspan=35, col=2, row=6, rowspan=23)

        widget = Widget(name='link_3', display_name='Link 3', font_size=16,template_file='text_widget.json',
                        type='link', colspan=2, col=4, row=5, rowspan=10)

        self.assertEquals(container.get_display_name(), "Container 33")
        self.assertEquals(container.get_template(), "container_widget.json")
        self.assertEquals(container.get_colspan(), 35)
        self.assertEquals(container.get_column(), 2)
        self.assertEquals(container.get_row(), 6)
        self.assertEquals(container.get_rowspan(), 23)

        container.add_widget(widget)

        self.assertEquals(container.get_widgets()[0].get_template(), "text_widget.json")

    def test_Page(self):
        page = Page(name='page_1', display_name='Page 1', template_file='page_template.json')

        container = Container(name='container_33', display_name='Container 33', template_file='container_widget.json',
                              colspan=4, col=12, row=4, rowspan=4)

        self.assertEquals(page.get_name(), 'page_1')
        self.assertEquals(page.get_display_name(), 'Page 1')
        self.assertEquals(page.get_template(), 'page_template.json')

        page.add_container(container)
        self.assertEquals(page.get_containers(), [container])

    def test_Dashboard(self):
        dashboard = Dashboard(wave_id=8, dashboard_name='HorizonCostAnalytics', dashboard_type='main',
                              display_name='Horizon Cost Analytics',
                              url='/services/data/v41.0/wave/dashboards/test', link_var='', group_name='1P',
                              folder_id='000123456', env='org62')

        page = Page(name='page_1', display_name='Page 1', template_file='page_template.json')

        self.assertEquals(dashboard.get_wave_id(), 8)
        self.assertEquals(dashboard.get_display_name(), "Horizon Cost Analytics")
        self.assertEquals(dashboard.get_dashboard_type(), "main")
        self.assertEquals(dashboard.get_url(), "/services/data/v41.0/wave/dashboards/test")
        self.assertEquals(dashboard.get_link_var(), "")
        self.assertEquals(dashboard.get_group_name(), "1P")
        self.assertEquals(dashboard.get_pages(), [])
        self.assertEquals(dashboard.get_env(), "org62")

        dashboard.add_page(page)

        self.assertEquals(dashboard.get_pages(), [page])
