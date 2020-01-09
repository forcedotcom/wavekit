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
from ds_generator.orm.EntityService import EntityService
from wave_common.utils import read_file, save_file, is_valid_json, exception_handler, Logger, filter_disabled
from ds_generator.types import *
from jinja2 import Template
import json
from jsonweb.encode import dumper


class WaveUIServices:
    def __init__(self, db_config, output, template_path, saql_path, env):
        self._entity_service = EntityService(db_config)
        self.output = output
        self.template_path = template_path
        self.saql_path = saql_path
        self.environment = env

    def populate_model_from_database(self, ds_name):
        """
        Method returns a list of Pages, and Dashboard name, belonging to provided Dashboard from the database
        :param wave_id:
        :return page_list, display_name:
        """
        display_name = self._entity_service.get_dashboard_by_name(ds_name).display_name
        page_list = self._entity_service.get_dashboard_pages(ds_name)
        for page in page_list:
            container_list = self._entity_service.get_page_containers(page.get_name())
            page.add_containers(container_list)
            for c in container_list:
                widget_list = self._entity_service.get_container_widgets(c.get_name())
                c.add_widgets(widget_list)
                for w in widget_list:
                    property_list = self._entity_service.get_widget_properties(w.get_name())
                    step_list = self._entity_service.get_widget_steps(w.get_name())
                    w.add_properties(property_list)
                    w.add_steps(step_list)
                    for p in step_list:
                        step_properties = self._entity_service.get_step_properties(p.get_name())
                        p.add_properties(step_properties)
        return page_list, display_name

    def generate_metadata(self, page_list, display_name):
        """
        Method outputs metadata file for a Dashboard based on a list of Pages and their content
        :param page_list:
        :param display_name:
        :return:
        """
        dashboard_pages = []
        for page in page_list:
            text_page = Page(page.get_name(), page.get_display_name(), page.get_template())
            dashboard_pages.append(text_page)
            for container in page.get_containers():
                #print (page.get_name())
                #print (container.get_name())
                text_container = Container(container.get_name(), container.get_display_name(), container.get_template(),
                                           container.get_colspan(), container.get_column(), container.get_row(),
                                           container.get_rowspan())
                text_page.add_container(text_container)

                for widget in container.get_widgets():
                    text_widget = Widget(widget.get_name(), widget.get_display_name(), widget.get_font_size(),
                                         widget.get_template(), widget.get_type(), widget.get_colspan(),
                                         widget.get_column(), widget.get_row(), widget.get_rowspan())
                    text_container.add_widget(text_widget)

                    for property in widget.get_properties():
                        text_prop = Property(property.get_id(), property.get_key(), property.get_value())
                        text_widget.add_property(text_prop)

                    for step in widget.get_steps():
                        text_step = Step(step.get_name(), step.get_display_name(), step.get_type(), step.get_template())
                        text_widget.add_step(text_step)

                        for property in step.get_properties():
                            step_prop = Property(property.get_id(), property.get_key(), property.get_value())
                            text_step.add_property(step_prop)

            json_content = dumper(dashboard_pages)
            save_file(self.output + "/" + display_name + "_dashboard_metadata.json", json_content)

    @staticmethod
    def data_replacement_json(file_name, dataset):
        """
        Method uses Jinja Templates to replace a set of values in provided JSON file and returns replaced JSON
        :param file_name:
        :param dataset:
        :return json:
        """
        template_file = read_file(file_name)
        template_file = template_file.replace('\\', 'BACKSLASH').replace('{{', 'OPEN_BRACKET').replace('}}', 'CLOSE_BRACKET')
        template_file = template_file.replace('{_{', '{{').replace('}_}', '}}')
        template = Template(template_file)
        json = template.render(dataset)
        json = json.replace('BACKSLASH', '\\').replace('OPEN_BRACKET', '{{').replace('CLOSE_BRACKET', '}}')
        return json

    # methods to generate sections of JSON
    def generate_page_json(self, name, display_name, template_file, widgets):
        """
        Method returns generated JSON for Page widgets based on provided template
        :param name:
        :param display_name:
        :param template_file:
        :param widgets:
        :return:
        """
        try:
            file_name = self.template_path + "/" + template_file
            dataset = {NAME: name, DISP_NAME: display_name, LAYOUTS: widgets}

            return self.data_replacement_json(file_name, dataset)
        except Exception as e:
            exception_handler("", e)

    def generate_container_json(self, template_file, widget_name):
        """
        Method returns generated JSON for Container widgets based on provided template
        :param template_file:
        :param widget_name:
        :return json:
        """
        try:
            file_name = self.template_path + "/" + template_file
            dataset = {WIDGET_NAME: widget_name, WIDGET_TYPE: "container"}

            return self.data_replacement_json(file_name, dataset)
        except Exception as e:
            exception_handler("", e)

    def generate_widget_step_json(self, template_file, dataset):
        """
        Method returns generated JSON for widgets/steps based on the provided template and dataset for replacement
        :param template_file:
        :param dataset:
        :return json:
        """
        try:
            file_name = self.template_path + "/" + template_file
            return self.data_replacement_json(file_name, dataset)
        except Exception as e:
            exception_handler("", e)

    def generate_saql_step_json(self, dashboard_name, saql_name, group_name):
        """
        Method returns generated SAQL for listselector type steps based on provided SAQL file
        :param dashboard_name:
        :param saql_name:
        :param group_name:
        :return saql:
        """
        try:
            file_name = self.saql_path + "/" + dashboard_name + "/" + saql_name
            dataset = {GROUP: group_name}

            return self.data_replacement_json(file_name, dataset)
        except Exception as e:
            exception_handler("", e)

    def generate_layouts_json(self, name, colspan, column, row, rowspan, style=""):
        """
        Method returns generated JSON layouts for widgets based on provided template
        :param name:
        :param colspan:
        :param column:
        :param row:
        :param rowspan:
        :param style:
        :return json:
        """
        try:
            file_name = self.template_path + "/widget_layout.json"
            dataset = {COLSPAN: colspan, COL: column, NAME: name, ROW: row, ROWSPAN: rowspan, STYLE: style}

            return self.data_replacement_json(file_name, dataset)
        except Exception as e:
            exception_handler("", e)

    def generate_dashboard_json(self, display_name, dashboard_name):
        """
        Method returns generated layouts, widgets, and steps JSON from metadata
        :param display_name:
        :param dashboard_name:
        :return layouts, widgets, steps:
        """
        try:
            #layouts = []
            widgets = []
            steps = []
            pages = []
            file_content = read_file(self.output + "/" + display_name + "_dashboard_metadata.json")
            metadata = json.loads(file_content)
            metadata.sort(key=lambda x: x[NAME].lower())

            for p_index, page in enumerate(metadata):
                layouts = []
                p_name = page[NAME]
                p_display = page[DISP_NAME]
                p_template = page[TEMPLATE]
                p_containers = page[CONTAINERS]

                for c_index, container in enumerate(p_containers):
                    c_name = container[NAME]
                    c_template = container[TEMPLATE]
                    c_widgets = container[WIDGETS]

                    layouts.append(
                        self.generate_layouts_json(c_name, container[COLSPAN], container[COL], container[ROW],
                                                   container[ROWSPAN])
                    )
                    # add widget_properties
                    for w_index, widget in enumerate(c_widgets):
                        w_name = widget[NAME]
                        w_display = widget[DISP_NAME]
                        w_steps = widget[STEPS]
                        w_properties = widget[PROPERTIES]
                        w_type = widget[TYPE]
                        w_template = widget[TEMPLATE]
                        w_font = widget[FONT_SIZE]

                        w_prop_dict = {}
                        for wp_index, w_property in enumerate(w_properties):
                            w_prop_dict[w_property[KEY]] = w_property[VAL]

                        # generating static text widgets
                        if w_type == STATIC_TEXT:
                            text_widget_dataset = {NAME: w_name, TEXT: w_prop_dict[TEXT], FONT_SIZE: w_font,
                                                   TEXT_CLR: w_prop_dict[TEXT_CLR], ALIGN: w_prop_dict[ALIGN]}
                            widgets.append(
                                self.generate_widget_step_json(w_template, text_widget_dataset)
                            )

                        # generating link widgets
                        if w_type == LINK:
                            link_widget_dataset = {NAME: w_name, DISP_NAME: w_display, URL: w_prop_dict[URL],
                                                   DEST_TYPE: w_prop_dict[DEST_TYPE], FONT_SIZE: w_font,
                                                   TEXT_CLR: w_prop_dict[TEXT_CLR], ALIGN: w_prop_dict[ALIGN],
                                                   DASH_LINK: w_prop_dict[self.environment + "_" + DASH_LINK]}
                            widgets.append(
                                self.generate_widget_step_json(w_template, link_widget_dataset)
                            )

                        # generating navigation widgets
                        if w_type == NAVIGATION:
                            nav_widget_dataset = {NAME: w_name, DISP_NAME: w_display, FONT_SIZE: w_font}
                            widgets.append(
                                self.generate_widget_step_json(w_template, nav_widget_dataset)
                            )

                        for s_index, step in enumerate(w_steps):
                            s_name = step[NAME]
                            s_prop = step[PROPERTIES]
                            s_type = step[TYPE]
                            s_template = step[TEMPLATE]

                            # generating listselector widgets
                            if w_type == LISTSELECTOR:
                                listselector_widget_dataset = {NAME: w_name, STEP_NAME: s_name, DISP_NAME: w_display}
                                widgets.append(
                                  self.generate_widget_step_json(w_template, listselector_widget_dataset)
                                )

                            if w_type == BAR_CHART:
                                # generating chart widgets
                                bar_chart_dataset = {NAME: w_name, STEP_NAME: s_name, BINS: w_prop_dict[BINS],
                                                     AXIS_MODE: w_prop_dict[AXIS_MODE], VIS_TYPE: w_prop_dict[VIS_TYPE],
                                                     CHART_TITLE: w_prop_dict[CHART_TITLE], TITLE_1: w_prop_dict[TITLE_1],
                                                     SUM: w_prop_dict[SUM], SHOW_TITLE: w_prop_dict[SHOW_TITLE],
                                                     SHOW_AXIS: w_prop_dict[SHOW_AXIS], SHOW_ACT: w_prop_dict[SHOW_ACT],
                                                     FONT_SIZE: w_font, COL_MAP: w_prop_dict[COL_MAP],
                                                     SHOW_LGND: w_prop_dict[SHOW_LGND]}
                                widgets.append(
                                    self.generate_widget_step_json(w_template, bar_chart_dataset)
                                )
                            if w_type == LINE_CHART:
                                # generating line chart widgets
                                line_chart_dataset = {NAME: w_name, STEP_NAME: s_name, AXIS_MODE: w_prop_dict[AXIS_MODE],
                                                      VIS_TYPE: w_prop_dict[VIS_TYPE], MEASURE: w_prop_dict[MEASURE],
                                                      SHOW_DASH: w_prop_dict[SHOW_DASH], FILL_AREA: w_prop_dict[FILL_AREA],
                                                      CHART_TITLE: w_prop_dict[CHART_TITLE], TITLE_1: w_prop_dict[TITLE_1],
                                                      SHOW_TITLE: w_prop_dict[SHOW_TITLE], SHOW_AXIS: w_prop_dict[SHOW_AXIS],
                                                      SHOW_ACT: w_prop_dict[SHOW_ACT], SHOW_LGND: w_prop_dict[SHOW_LGND],
                                                      SHOW_ZERO: w_prop_dict[SHOW_ZERO], FONT_SIZE: w_font}
                                widgets.append(
                                    self.generate_widget_step_json(w_template, line_chart_dataset)
                                )

                            if s_type == CHART:
                                ch_prop_dict = {}
                                for ch_index, ch_property in enumerate(s_prop):
                                    ch_prop_dict[ch_property[KEY]] = ch_property[VAL]

                                saql_json = self.saql_path + "/" + dashboard_name + "/" + ch_prop_dict[SAQL_NAME]
                                saql_json = read_file(saql_json)
                                saql_json = json.dumps(saql_json).strip('"')
                                # generation of chart steps
                                if w_type == BAR_CHART or w_type == LINE_CHART:
                                    chart_step_dataset = {STEP_NAME: s_name, SAQL_QUERY: saql_json,
                                                          AXIS_MODE: w_prop_dict[AXIS_MODE], VIS_TYPE: w_prop_dict[VIS_TYPE],
                                                          CHART_TITLE: w_prop_dict[CHART_TITLE], TITLE_1: w_prop_dict[TITLE_1],
                                                          SHOW_TITLE: w_prop_dict[SHOW_TITLE], SHOW_AXIS: w_prop_dict[SHOW_AXIS],
                                                          SHOW_ACT: w_prop_dict[SHOW_ACT], FONT_SIZE: w_font,
                                                          SHOW_LGND: w_prop_dict[SHOW_LGND]}
                                else:
                                    chart_step_dataset = {STEP_NAME: s_name, SAQL_QUERY: saql_json}

                                steps.append(
                                    self.generate_widget_step_json(s_template, chart_step_dataset)
                                )

                                # generation of cost bucket/MoM calculations
                                if w_type == DYN_TEXT:
                                    dyn_text_dataset = {NAME: w_name, STEP_NAME: s_name, VAR: ch_prop_dict[VAR],
                                                        FONT_SIZE: w_font}
                                    widgets.append(
                                        self.generate_widget_step_json(w_template, dyn_text_dataset)
                                    )

                                if w_type == NUM:
                                    num_dataset = {NAME: w_name, STEP_NAME: s_name, VAR: ch_prop_dict[VAR],
                                                   COMPACT: ch_prop_dict[COMPACT], FONT_SIZE: w_font}
                                    widgets.append(
                                        self.generate_widget_step_json(w_template, num_dataset)
                                    )

                            # for dropdown/filtering steps
                            else:
                                s_prop_dict = {}
                                for p_index, property in enumerate(s_prop):
                                    s_prop_dict[property[KEY]] = property[VAL]
                                saql_json = self.generate_saql_step_json(dashboard_name, s_prop_dict[SAQL_NAME],
                                                                                      s_prop_dict[GROUP])
                                saql_json = json.dumps(saql_json).strip('"')
                                listselector_step_dataset = {STEP_NAME: s_name, GROUP: s_prop_dict[GROUP], SAQL_QUERY: saql_json,
                                                             SELECT_MODE: s_prop_dict[SELECT_MODE]}
                                steps.append(
                                    self.generate_widget_step_json(s_template, listselector_step_dataset)
                                )

                        layouts.append(
                            self.generate_layouts_json(w_name, widget[COLSPAN], widget[COL], widget[ROW],
                                                       widget[ROWSPAN], w_prop_dict.get(STYLE, ""))
                        )
                    widgets.append(
                        self.generate_container_json(c_template, c_name)
                    )

                layouts = ",".join(layouts)

                pages.append(
                    self.generate_page_json(p_name, p_display, p_template, layouts)
                )

            widgets = ",".join(widgets)
            steps = ",".join(steps)
            pages = ",".join(pages)

            return pages, widgets, steps

        except Exception as e:
            exception_handler("", e)

    def run(self, ds_name):
        """
        Method inserts layouts, widgets, steps into provided dashboard template and outputs to file; returns file name
        :param wave_id:
        :return file_name:
        """
        display_name = self._entity_service.get_dashboard_by_name(ds_name).display_name
        dashboard_name = self._entity_service.get_dashboard_by_name(ds_name).dashboard_name
        file_name = self.template_path + "/dashboard_template.json"
        page_content, widget_content, step_content = self.generate_dashboard_json(display_name, dashboard_name)

        try:
            data = {
                "dashboard_name": display_name,
                "pages": page_content,
                "steps": step_content,
                "widgets": widget_content,
                "folder_id": self._entity_service.get_dashboard_by_name(ds_name).folder_id
            }
            dashboard_content = self.data_replacement_json(file_name, data)
        except Exception as e:
            exception_handler("", e)

        file_name = self.output + "/" + display_name + "_dashboard_dataset_replacement.json"
        save_file(file_name, dashboard_content)
        return file_name

    def execute(self, ds_name):
        """
        Method calls previous methods to generate complete dashboard JSON from metadata; returns file name
        :param wave_id:
        :return file_name:
        """
        container_list, display_name = self.populate_model_from_database(ds_name)
        self.generate_metadata(container_list, display_name)
        return self.run(ds_name)
