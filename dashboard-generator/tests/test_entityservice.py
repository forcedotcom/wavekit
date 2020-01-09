"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import unittest
from ds_generator.orm.EntityService import EntityService
from ds_generator.Models import Property, Step, Widget, Container, Dashboard, Dataset, Page
from ds_generator.orm.EntityModels import StepEntity, StepPropertyEntity, WidgetEntity, WidgetPropertyEntity, \
    ContainerEntity, DashboardEntity, DatasetEntity, PageEntity


class EntityServiceTestSuite(unittest.TestCase):
    def test_Step_Property_funcs(self):
        es = EntityService()

        StepPropertyEntity.metadata.create_all(es.engine)

        # adding a step_property
        step_property = Property(id=5, key='saql_name', value='active_asset.saql')

        es.add_property_to_step(step_property, 'step_33')

        self.assertEqual(es.get_step_properties(step_name='step_33')[0].id, step_property.id)

    def test_Widget_Property_funcs(self):
        es = EntityService()

        WidgetPropertyEntity.metadata.create_all(es.engine)

        # adding a widget property
        widget_property = Property(id=3, key='text', value='This is a dashboard')

        es.add_property_to_widget(widget_property, 'widget_1')

        self.assertEqual(es.get_widget_properties(widget_name='widget_1')[0].id, widget_property.id)

    def test_Step_funcs(self):
        es = EntityService()

        StepEntity.metadata.create_all(es.engine)

        StepPropertyEntity.metadata.create_all(es.engine)

        step = Step(name='Kingdom_1', display_name='Kingdom 1', type='', template_file='listselector_step.json' )

        property_1 = Property(id=5, key='group_name', value='kingdom')

        property_2 = Property(id=11, key='saql_name', value='listselector_step.saql')

        # adding
        es.add_step_to_widget(step, 'text_2')
        es.add_property_to_step(property_1, 'step_3')
        es.add_property_to_step(property_2, 'step_3')

        self.assertEqual(es.get_widget_steps(widget_name='text_2')[0].display_name, step.display_name)
        self.assertEqual(es.get_step_properties(step_name='step_3')[0].id, property_1.id)
        self.assertEqual(es.get_step_properties(step_name='step_3')[1].id, property_2.id)

        properties_keys = []

        properties = es.get_step_properties(step_name='step_3')

        for property in properties:
            properties_keys.append(property.key)
        self.assertEqual(properties_keys, ['group_name', 'saql_name'])

    def test_Widget_funcs(self):
        es = EntityService()

        WidgetEntity.metadata.create_all(es.engine)

        StepEntity.metadata.create_all(es.engine)

        WidgetPropertyEntity.metadata.create_all(es.engine)

        # adding components
        widget_1 = Widget(name='link_2', display_name='Link 2', font_size=14, template_file='link_widget.json',
                          type='link', colspan=1, col=1, row=2, rowspan=2)

        widget_2 = Widget(name='chart_1', display_name='Chart 1', font_size=0, template_file='bar_chart_widget.json',
                          type='chart', colspan=20, col=3, row=5, rowspan=10)

        step = Step(name='step_3', display_name='Step 3', type='chart', template_file='chart_step.json')

        w_property_1 = Property(id=5, key='dest_name', value='https://gus.my.salesforce.com/apex/Service_Catalog')

        w_property_2 = Property(id=11, key='dest_type', value='url')

        es.add_widget_to_container(widget_1, 'container_21')
        es.add_widget_to_container(widget_2, 'container_21')
        es.add_step_to_widget(step, 'chart_1')
        es.add_property_to_widget(w_property_1, 'chart_1')
        es.add_property_to_widget(w_property_2, 'chart_1')

        # assertions
        widget_names = []
        widget_list = es.get_container_widgets(container_name='container_21')

        for w in widget_list:
            widget_names.append(w.display_name)

        self.assertEqual(widget_names, ['Link 2', 'Chart 1'])
        self.assertEqual(es.get_widget_steps(widget_name=widget_2.name)[0].type, step.type)
        self.assertEqual(es.get_widget_properties(widget_name=widget_2.name)[1].value, "url")
        self.assertEqual(es.get_widget_properties(widget_name=widget_1.name), [])

    def test_Page_funcs(self):
        es = EntityService()

        PageEntity.metadata.create_all(es.engine)

        ContainerEntity.metadata.create_all(es.engine)

        # adding components
        page_1 = Page(name='page_1', display_name='Page 1', template_file='page_template.json')

        container_4 = Container(name='container_4', display_name='Container 4', template_file='container_widget.json',
                                colspan=0, col=0, row=9, rowspan=8)

        es.add_page(page_1)
        es.add_container_to_page(container_4, 'page_1')

        self.assertEqual(es.get_page_containers(page_name=page_1.name)[0].name, 'container_4')

    def test_Container_funcs(self):
        es = EntityService()

        ContainerEntity.metadata.create_all(es.engine)

        WidgetEntity.metadata.create_all(es.engine)

        # adding components
        container_1 = Container(name='container_4', display_name='Container 4', template_file='container_widget.json',
                                colspan=0, col=0, row=9, rowspan=8)

        container_2 = Container(name='container_5', display_name='Container 5', template_file='container_widget.json',
                                colspan=5, col=10, row=18, rowspan=1)

        widget_1 = Widget(name='link_2', display_name='Link 2', font_size=10, template_file='link_widget.json',
                          type='link', colspan=0, col=0, row=9, rowspan=8)

        widget_2 = Widget(name='chart_1', display_name='Chart 1', font_size=0, template_file='bar_chart_widget.json',
                          type='chart', colspan=5, col=10, row=18, rowspan=1)

        es.add_container_to_page(container_1, 'page_1')
        es.add_container_to_page(container_2, 'page_1')
        es.add_widget_to_container(widget_1, 'container_4')
        es.add_widget_to_container(widget_2, 'container_5')

        self.assertEqual(es.get_container_widgets(container_name=container_1.name)[0].name, 'link_2')
        self.assertEqual(es.get_container_widgets(container_name='container_5')[0].rowspan, widget_2.rowspan)

    def test_Dashboard_funcs(self):
        es = EntityService()

        DashboardEntity.metadata.create_all(es.engine)

        dashboard_1 = Dashboard(wave_id="dashboard_2", dashboard_name='1P', dashboard_type='main',
                                display_name='1P Dashboard', url='/services/data/v41.0/wave/dashboards/test',
                                link_var='', group_name='', folder_id='0000123456', env='sandbox')

        dashboard_2 = Dashboard(wave_id="dashboard_8", dashboard_name='MoFo', dashboard_type='main',
                                display_name='MoFo Dashboard', url='/services/data/v41.0/wave/dashboards/test',
                                link_var='', group_name='', folder_id='0000123456', env='sandbox')

        page_1 = Page(name='page_1', display_name='Page 1', template_file='page_template.json')

        dashboard_2.add_page(page_1)
        es.add_new_dashboard(dashboard_1)
        es.add_new_dashboard(dashboard_2)
        es.add_page(page_1)
        es.add_relationship("1P", "page_1")

        dashboards = es.get_dashboards_by_env("sandbox")
        dashboard_names = []

        for dashboard in dashboards:
            dashboard_names.append(dashboard.dashboard_name)

        self.assertEqual(es.get_dashboard_pages("1P")[0].name, "page_1")
        self.assertEqual(dashboard_names, ['1P', 'MoFo'])
        self.assertEqual(es.get_dashboards_by_env("sandbox")[0].wave_id, dashboard_1.wave_id)

    def test_Dataset_funcs(self):
        es = EntityService()

        DatasetEntity.metadata.create_all(es.engine)

        dataset_1 = Dataset(id=1, type='period', name='period', env='org62')

        es.add_dataset(dataset_1)

        self.assertEqual(len(es.get_datasets_by_env("org62")), 1)
        self.assertEqual(es.get_datasets_by_env("org62")[0].name, "period")
