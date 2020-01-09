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
import json
import mock
import os

from wave_common.utils import read_file
from ds_generator.Models import Property, Step, Widget, Container, Dashboard, Page
from ds_generator.orm.EntityModels import StepEntity, StepPropertyEntity, WidgetEntity, WidgetPropertyEntity, \
    ContainerEntity, DashboardEntity
from ds_generator.WaveUiServices import WaveUIServices
from ds_generator.types import *


class WaveUIServiceTestSuite(unittest.TestCase):
    def setUp(self):
        # mock db_config
        self.mock_db_config = mock.Mock(username="username",
                                        password="password",
                                        host="localhost",
                                        database="database")
        self.output = 'tests/output'
        self.template_path = 'tests/templates'
        self.saql_path = 'tests/saql'
        self.environment = 'sandbox'

        self.generator = WaveUIServices(None, self.output, self.template_path, self.saql_path, self.environment)

        # mock db population
        StepPropertyEntity.metadata.create_all(self.generator._entity_service.engine)
        StepEntity.metadata.create_all(self.generator._entity_service.engine)
        WidgetPropertyEntity.metadata.create_all(self.generator._entity_service.engine)
        WidgetEntity.metadata.create_all(self.generator._entity_service.engine)
        ContainerEntity.metadata.create_all(self.generator._entity_service.engine)

        dashboard_1 = Dashboard('wave_id_test_1', 'Dashboard1', 'dashboard_type', 'Dashboard #1',
                                'url', 'link_var', 'group_name', 'folder_id', 'sandbox')

        page_1 = Page('page_1', 'Page 1', 'page_template.json')
        page_2 = Page('page_2', 'Page 2', 'page_template.json')

        container_2 = Container('container_2', 'Dropdown Container', 'container_widget.json', 4, 34, 2, 9)
        listselector_10 = Widget('listselector_10', 'Kingdom', 0, 'listselector_widget.json', 'listselector', 4, 34, 5, 1)
        kingdom_1 = Step('kingdom_1', 'kingdom 1', '', 'listselector_step.json')
        kingdom_prop_1 = Property(1, 'group_name', 'kingdom')
        kingdom_prop_2 = Property(2, 'saql_name', 'listselector_step.saql')
        kingdom_prop_3 = Property(3, 'select_mode', 'multi')

        container_4 = Container('container_4', 'Side links containers', 'container_widget.json', 6, 0, 1, 15)
        text_15 = Widget('text_15', 'Text 15', 16, 'text_widget.json', 'static_text', 6, 0, 1, 1,)
        text_1_prop_1 = Property(4, 'text', 'Core CRM')
        text_1_prop_2 = Property(5, 'text_colour', 'rgb(1, 73, 157)')
        text_1_prop_3 = Property(6, 'alignment', 'left')
        text_1_prop_4 = Property(7, 'style', '"backgroundColor": "#091A3E","borderEdges": ["bottom"]')

        container_6 = Container('container_6', 'Chart #1 Section', 'container_widget.json', 28, 6, 6, 6)
        chart_5 = Widget('chart_5', 'Cost Type Series', 14, 'bar_chart_widget.json', 'bar_chart', 25, 9, 6, 6)
        Period_Year_Period_M_1 = Step('Period_Year_Period_M_1', 'Period Year Period', 'chart', 'chart_widget_step.json')
        pypm_prop_1 = Property(8, 'saql_name', 'period_year_period_m.saql')
        chart_5_prop_1 = Property(9, 'bins', ' ')
        chart_5_prop_2 = Property(10, 'axis_mode', 'sync')
        chart_5_prop_3 = Property(11, 'vis_type', 'stackvbar')
        chart_5_prop_4 = Property(12, 'chart_title', 'Monthly Cost')
        chart_5_prop_5 = Property(13, 'title_1', 'Full Cost')
        chart_5_prop_6 = Property(14, 'sum', 'none')
        chart_5_prop_7 = Property(15, 'show_title', 'true')
        chart_5_prop_8 = Property(16, 'show_axis', 'true')
        chart_5_prop_9 = Property(17, 'show_action', 'true')
        chart_5_prop_10 = Property(18, 'show_legend', 'true')
        chart_5_prop_11 = Property(19, 'col_map', ' ')

        listselector_1 = Widget('listselector_1', 'Period', 0, 'listselector_widget.json', 'listselector', 4, 34, 2, 1);
        Period_3 = Step('Period_3', 'Period 3', 'chart', 'chart_step.json')
        Period_prop_1 = Property(20, 'saql_name', 'period_step_query.saql')
        Period_prop_2 = Property(21, 'select_mode', 'multi')

        container_5 = Container('container_5', 'Top space', 'container_widget.json', 28, 6, 1, 1)

        link_1 = Widget('link_1', 'Help', 14, 'link_widget.json', 'link', 4, 34, 1, 1)
        link_prop_1 = Property(22, 'url', 'https://docs.google.com/document')
        link_prop_2 = Property(23, 'dest_type', 'url')
        link_prop_3 = Property(24, 'text_colour', '#FFFFFF')
        link_prop_4 = Property(25, 'alignment', 'left')
        link_prop_5 = Property(26, 'sandbox_dash_link', 'Wave_Test_1')

        text_12 = Widget('text_12', 'Infra Cost MoM', 16, 'calculation_text_widget.json', 'dynamic_text', 4, 9, 5, 1)
        lens_4 = Step('lens_4', 'Lens 4', 'chart', 'chart_step.json')
        lens_prop_1 = Property(27, 'saql_name', 'listselector_step.saql')
        lens_prop_2 = Property(28, 'var_name', 'mom')

        self.generator._entity_service.add_new_dashboard(dashboard_1)
        self.generator._entity_service.add_page(page_1)
        self.generator._entity_service.add_page(page_2)
        self.generator._entity_service.add_container_to_page(container_2, 'page_1')
        self.generator._entity_service.add_widget_to_container(listselector_1, 'container_2')
        self.generator._entity_service.add_step_to_widget(Period_3, 'listselector_1')
        self.generator._entity_service.add_property_to_step(Period_prop_1, 'Period_3')
        self.generator._entity_service.add_property_to_step(Period_prop_2, 'Period_3')

        self.generator._entity_service.add_widget_to_container(listselector_10, 'container_2')
        self.generator._entity_service.add_step_to_widget(kingdom_1, 'listselector_10')
        self.generator._entity_service.add_property_to_step(kingdom_prop_1, 'kingdom_1')
        self.generator._entity_service.add_property_to_step(kingdom_prop_2, 'kingdom_1')
        self.generator._entity_service.add_property_to_step(kingdom_prop_3, 'kingdom_1')

        self.generator._entity_service.add_container_to_page(container_4, 'page_1')
        self.generator._entity_service.add_widget_to_container(text_15, 'container_4')
        self.generator._entity_service.add_property_to_widget(text_1_prop_1, 'text_15')
        self.generator._entity_service.add_property_to_widget(text_1_prop_2, 'text_15')
        self.generator._entity_service.add_property_to_widget(text_1_prop_3, 'text_15')
        self.generator._entity_service.add_property_to_widget(text_1_prop_4, 'text_15')

        self.generator._entity_service.add_container_to_page(container_5, 'page_1')
        self.generator._entity_service.add_widget_to_container(link_1, 'container_5')
        self.generator._entity_service.add_property_to_widget(link_prop_1, 'link_1')
        self.generator._entity_service.add_property_to_widget(link_prop_2, 'link_1')
        self.generator._entity_service.add_property_to_widget(link_prop_3, 'link_1')
        self.generator._entity_service.add_property_to_widget(link_prop_4, 'link_1')
        self.generator._entity_service.add_property_to_widget(link_prop_5, 'link_1')
        self.generator._entity_service.add_widget_to_container(text_12, 'container_5')
        self.generator._entity_service.add_step_to_widget(lens_4, 'text_12')
        self.generator._entity_service.add_property_to_step(lens_prop_1, 'lens_4')
        self.generator._entity_service.add_property_to_step(lens_prop_2, 'lens_4')

        self.generator._entity_service.add_container_to_page(container_6, 'page_1')
        self.generator._entity_service.add_widget_to_container(chart_5, 'container_6')
        self.generator._entity_service.add_step_to_widget(Period_Year_Period_M_1, 'chart_5')
        self.generator._entity_service.add_property_to_step(pypm_prop_1, 'Period_Year_Period_M_1')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_1, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_2, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_3, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_4, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_5, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_6, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_7, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_8, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_9, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_10, 'chart_5')
        self.generator._entity_service.add_property_to_widget(chart_5_prop_11, 'chart_5')

        self.generator._entity_service.add_relationship('Dashboard1', 'page_1')
        self.generator._entity_service.add_relationship('Dashboard1', 'page_2')

    def test_populate_metamodel(self):
        page_list, dashboard_name = self.generator.populate_model_from_database('Dashboard1')

        p_names = []
        for page in page_list:
            p_names.append(page.name)
        p_names.sort()

        self.assertEquals(len(page_list), 2)
        self.assertEquals(p_names, ['page_1', 'page_2'])

    def test_metadata_generation(self):
        container_list, dashboard_name = self.generator.populate_model_from_database('Dashboard1')

        self.generator.generate_metadata(container_list, dashboard_name)

        # check that path exists
        self.assertTrue(os.path.exists(self.output + "/" + dashboard_name + "_dashboard_metadata.json"))

        # check that one metadata file was generated
        self.assertEquals(len(os.listdir(self.output)), 2)

        # check contents
        metamodel_dict = json.loads(read_file(os.path.join(self.output, dashboard_name + "_dashboard_metadata.json")))
        self.assertEquals(len(metamodel_dict), len(container_list))

        content = list(filter(lambda x: x["name"] == "text_15", metamodel_dict[0]["containers"][1]["widgets"]))
        self.assertEquals(len(content), 1)  # is one container
        self.assertTrue("properties" in content[0] and len(content[0]["properties"]) == 4)
        self.assertEquals((sorted(map(lambda x: x["key"], content[0]["properties"]))),
                          ["alignment", "style", "text", "text_colour"])

    def test_data_replacement(self):
        file_name = self.template_path + "/text_widget_dynamic.json"
        dataset = {'name': 'widget_1', 'font_size': 20, 'step_name': 'step_2', 'var_name': 'count'}
        json_output = self.generator.data_replacement_json(file_name, dataset)
        replacement = json.loads("{" + json_output + "}")

        dyn_text_dataset = {NAME: "widget_1", STEP_NAME: "step_2", VAR: "count", FONT_SIZE: 20}
        dynamic_text_json = self.generator.generate_widget_step_json("text_widget_dynamic.json", dyn_text_dataset)

        link_widget_dataset = {NAME: "link_3", DISP_NAME: "Help", URL: "https://link.ca", DEST_TYPE: "url", FONT_SIZE: 34,
                               TEXT_CLR: "red", ALIGN: "center", DASH_LINK: "Wave_ID_Test"}
        link_json = self.generator.generate_widget_step_json("link_widget.json", link_widget_dataset)

        link_json = json.loads("{" + link_json + "}")

        # print json_output
        params = replacement["widget_1"]["parameters"]

        self.assertEquals(params["fontSize"], 20)
        self.assertEquals(params["text"], "{{cell(step_2.selection, 0, \"count\").asString()}}")
        self.assertEquals(json_output, dynamic_text_json)

        self.assertEquals(link_json["link_3"]["parameters"]["destinationType"], "url")

    def test_generate_json(self):
        self.generator.execute('Dashboard1')
        name = self.generator._entity_service.get_dashboard_by_name('Dashboard1').display_name

        # check paths
        self.assertTrue(os.path.exists(self.output))
        self.assertEquals(len(os.listdir(self.output)), 2)
        self.assertEquals(sorted(os.listdir(self.output)), [name + "_dashboard_dataset_replacement.json",
                                                            name + "_dashboard_metadata.json"])

        # check content
        file_name = name + "_dashboard_dataset_replacement.json"
        content_dict = json.loads(read_file(os.path.join(self.output, file_name)))
        self.assertTrue("label" in content_dict and content_dict["label"] == name)
        self.assertTrue("state" in content_dict)

        # check state_content
        state_content = content_dict["state"]
        self.assertTrue("dataSourceLinks" in state_content and "gridLayouts" in state_content)

        # layouts
        layouts_content = content_dict["state"]["gridLayouts"][0]["pages"][0]["widgets"]
        print (content_dict["state"]["gridLayouts"][0]["pages"][0])
        layouts_dict = {}

        for layout in layouts_content:
            name = layout["name"]
            layouts_dict[name] = layout

        self.assertEquals(len(layouts_content), 10)

        self.assertTrue("column" in layouts_dict["container_2"] and
                        "colspan" in layouts_dict["container_2"] and
                        "row" in layouts_dict["container_2"] and
                        "rowspan" in layouts_dict["container_2"] and
                        "name" in layouts_dict["container_2"])

        # checking properties of layout
        self.assertEquals(layouts_dict["container_5"]["row"], 1)
        self.assertEquals(layouts_dict["listselector_1"]["column"], 34)

        # check steps
        self.assertEquals(len(content_dict["state"]["steps"]), 4)
        step = content_dict["state"]["steps"]["Period_3"]

        self.assertTrue("groups" in step and
                        "label" in step and
                        "numbers" in step and
                        "query" in step and
                        "selectMode" in step and
                        "strings" in step and
                        "type" in step and
                        "useGlobal" in step and
                        "visualizationParameters" in step)

        self.assertEquals(step["selectMode"], "singlerequired")

        # check step properties
        step = content_dict["state"]["steps"]["kingdom_1"]
        self.assertEquals(step["selectMode"], "multi")

        # check widgets
        widgets_dict = content_dict["state"]["widgets"]
        self.assertEquals(len(widgets_dict), 10)

        self.assertTrue("type" in widgets_dict["container_2"] and
                        "parameters" in widgets_dict["container_2"] and
                        "alignmentX" in widgets_dict["container_2"]["parameters"] and
                        "alignmentY" in widgets_dict["container_2"]["parameters"])

        self.assertTrue("type" in widgets_dict["text_15"] and
                        "parameters" in widgets_dict["text_15"] and
                        "text" in widgets_dict["text_15"]["parameters"] and
                        "fontSize" in widgets_dict["text_15"]["parameters"] and
                        "showActionMenu" in widgets_dict["text_15"]["parameters"])

        self.assertEquals(widgets_dict["listselector_1"]["parameters"]["step"], "Period_3")
        self.assertEquals(widgets_dict["text_15"]["parameters"]["textColor"], "rgb(1, 73, 157)")

