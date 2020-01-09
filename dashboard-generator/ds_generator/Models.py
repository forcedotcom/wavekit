"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from jsonweb.encode import to_object

"""
PROPERTY: represents additional properties of Steps or Widgets

 ex. a Widget with type=link would have a destination/url
   - example property object would have key='destination', value="url_of_the_link"
"""
@to_object()
class Property:
    def __init__(self, id, key, value):
        self.id = id
        self.key = key
        self.value = value

    def get_id(self):
        return self.id

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


"""
STEP: contains a query (dynamic)/static data to be used within a Widget
    - if Step has "static" type then Property is a KVP of the name and data
    - if Step has "dynamic" type then Properties examples are key="template_file", value="basic_layout.json"  
"""
@to_object()
class Step:
    def __init__(self, name, display_name, type, template_file):
        self.name = name
        self.display_name = display_name
        self.type = type
        self.template_file = template_file
        self.properties = []

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_type(self):
        return self.type

    def get_template(self):
        return self.template_file

    def get_properties(self):
        return self.properties

    def add_properties(self, list):
        return self.properties.extend(list)

    def add_property(self, property):
        return self.properties.append(property)


"""
WIDGET: representing different types of dashboard widgets (link, chart, text, etc.). 
Has:
    - type-specific properties 
    - steps   
"""
@to_object()
class Widget:
    def __init__(self, name, display_name, font_size, template_file, type, colspan, col, row, rowspan):
        self.name = name
        self.display_name = display_name
        self.font_size = font_size
        self.template_file = template_file
        self.type = type
        self.colspan = colspan
        self.col = col
        self.row = row
        self.rowspan = rowspan
        self.properties = []
        self.steps = []

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_font_size(self):
        return self.font_size

    def get_template(self):
        return self.template_file

    def get_type(self):
        return self.type

    def get_colspan(self):
        return self.colspan

    def get_column(self):
        return self.col

    def get_row(self):
        return self.row

    def get_rowspan(self):
        return self.rowspan

    def get_properties(self):
        return self.properties

    def add_properties(self, list):
        return self.properties.extend(list)

    def add_property(self, property):
        return self.properties.append(property)

    def get_steps(self):
        return self.steps

    def add_steps(self, list):
        return self.steps.extend(list)

    def add_step(self, step):
        return self.steps.append(step)


"""
CONTAINER: all Widgets belong to a Container, collection of one or more Widgets
"""
@to_object()
class Container:
    def __init__(self, name, display_name, template_file, colspan, col, row, rowspan):
        self.name = name
        self.display_name = display_name
        self.template_file = template_file
        self.colspan = colspan
        self.col = col
        self.row = row
        self.rowspan = rowspan
        self.widgets = []
        self.pages = []

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_template(self):
        return self.template_file

    def get_colspan(self):
        return self.colspan

    def get_column(self):
        return self.col

    def get_row(self):
        return self.row

    def get_rowspan(self):
        return self.rowspan

    def get_widgets(self):
        return self.widgets

    def add_widgets(self, list):
        return self.widgets.extend(list)

    def add_widget(self, widget):
        return self.widgets.append(widget)

    def remove_widget(self, widget):
        return self.widgets.remove(widget)

    def get_pages(self):
        return self.pages

    def add_pages(self, list):
        return self.pages.extend(list)

    def add_page(self, page):
        return self.pages.append(page)

    def remove_page(self, page):
        return self.pages.remove(page)


"""
PAGE: has Containers
"""
@to_object()
class Page:
    def __init__(self, name, display_name, template_file):
        self.name = name
        self.display_name = display_name
        self.template_file = template_file
        self.containers = []
        self.dashboards = []

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_template(self):
        return self.template_file

    def get_containers(self):
        return self.containers

    def add_containers(self, list):
        return self.containers.extend(list)

    def add_container(self, container):
        return self.containers.append(container)

    def remove_container(self, container):
        return self.containers.remove(container)

    def get_dashboards(self):
        return self.dashboards

    def add_dashboards(self, list):
        return self.dashboards.extend(list)

    def add_dashboard(self, dashboard):
        return self.dashboards.append(dashboard)

    def remove_dashboard(self, dashboard):
        return self.dashboards.remove(dashboard)

"""
DASHBOARD: has Pages
"""
@to_object()
class Dashboard:
    def __init__(self, wave_id, dashboard_name, dashboard_type, display_name, url, link_var, group_name,
                 folder_id, env):
        self.wave_id = wave_id
        self.dashboard_name = dashboard_name
        self.dashboard_type = dashboard_type
        self.display_name = display_name
        self.url = url
        self.link_var = link_var
        self.group_name = group_name
        self.folder_id = folder_id
        self.env = env
        self.pages = []

    def get_wave_id(self):
        return self.wave_id

    def get_dashboard_name(self):
        return self.dashboard_name

    def get_display_name(self):
        return self.display_name

    def get_url(self):
        return self.url

    def get_link_var(self):
        return self.link_var

    def get_dashboard_type(self):
        return self.dashboard_type

    def get_group_name(self):
        return self.group_name

    def get_folder_id(self):
        return self.folder_id

    def get_env(self):
        return self.env

    def get_pages(self):
        return self.pages

    def add_pages(self, list):
        return self.pages.extend(list)

    def add_page(self, page):
        return self.pages.append(page)

    def remove_page(self, page):
        return self.pages.remove(page)


"""
DATASET: datasets that are used in the dashboard
"""
@to_object()
class Dataset:
    def __init__(self, id, type, name, env):
        self.id = id
        self.type = type
        self.name = name
        self.env = env

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_env(self):
        return self.env


