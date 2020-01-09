"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

EntityBase = declarative_base()


class StepEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'steps'
    name = Column(String(250), primary_key=True)
    display_name = Column(String(250))
    widget_name = Column(String(250), ForeignKey('widgets.name'))
    type = Column(String(250))
    template_file = Column(String(250))
    properties = relationship("StepPropertyEntity")

    def __init__(self, name='', widget_name='', display_name='', type='', template_file='', properties=[]):
        self.name = name
        self.widget_name = widget_name
        self.display_name = display_name
        self.type = type
        self.template_file = template_file
        self.properties = properties


class StepPropertyEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'step_property'
    id = Column(Integer, primary_key=True)
    step_name = Column(String(250), ForeignKey('steps.name'))
    key = Column(String(250))
    value = Column(String(250))

    def __init__(self, id=None, step_name='', key='', value=''):
        self.id = id
        self.step_name = step_name
        self.key = key
        self.value = value


class AssociationEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'page_dashboard_relationship'
    dashboard_name = Column(String(250), ForeignKey('dashboard.dashboard_name'), primary_key=True)
    page_name = Column(String(250), ForeignKey('page.name'), primary_key=True)
    page = relationship("PageEntity", back_populates="dashboards")
    dashboard = relationship("DashboardEntity", back_populates="pages")

    def __init__(self, dashboard_name='', page_name=''):
        self.dashboard_name = dashboard_name
        self.page_name = page_name


class PageEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'page'
    name = Column(String(250), primary_key=True)
    display_name = Column(String(250))
    template_file = Column(String(250))
    containers = relationship("ContainerEntity")
    dashboards = relationship("AssociationEntity", back_populates="page")

    def __init__(self, name='', display_name='', template_file='', containers=[], dashboards=[]):
        self.name = name
        self.display_name = display_name
        self.template_file = template_file
        self.containers = containers
        self.dashboards = dashboards


class ContainerEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'container_widget'
    name = Column(String(250), primary_key=True)
    display_name = Column(String(250))
    template_file = Column(String(250))
    page_name = Column(String(250), ForeignKey('page.name'))
    colspan = Column(Integer)
    col = Column(Integer)
    row = Column(Integer)
    rowspan = Column(Integer)
    widgets = relationship("WidgetEntity")

    def __init__(self, name='', display_name='', template_file='', page_name='', colspan=None, col=None, row=None,
                 rowspan=None, widgets=[], pages=[]):
        self.name = name
        self.display_name = display_name
        self.template_file = template_file
        self.page_name = page_name
        self.colspan = colspan
        self.col = col
        self.row = row
        self.rowspan = rowspan
        self.widgets = widgets
        self.pages = pages


class WidgetEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'widgets'
    name = Column(String(250), primary_key=True)
    display_name = Column(String(250))
    container_name = Column(String(250), ForeignKey('container_widget.name'))
    font_size = Column(Integer)
    template_file = Column(String(250))
    type = Column(String(250))
    colspan = Column(Integer)
    col = Column(Integer)
    row = Column(Integer)
    rowspan = Column(Integer)
    properties = relationship("WidgetPropertyEntity")
    steps = relationship("StepEntity")

    def __init__(self, name='', display_name='', container_name='', font_size=None, template_file='', type='',
                 colspan=None, col=None, row=None, rowspan=None, properties=[], steps=[]):
        self.name = name
        self.display_name = display_name
        self.container_name = container_name
        self.font_size = font_size
        self.template_file = template_file
        self.type = type
        self.colspan = colspan
        self.col = col
        self.row = row
        self.rowspan = rowspan
        self.properties = properties
        self.steps = steps


class WidgetPropertyEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'widget_property'
    id = Column(Integer, primary_key=True)
    widget_name = Column(Integer, ForeignKey('widgets.name'))
    key = Column(String(250))
    value = Column(String(250))

    def __init__(self, id=None, widget_name='', key='', value=''):
        self.id = id
        self.widget_name = widget_name
        self.key = key
        self.value = value
        self.value = value


class DashboardEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'dashboard'
    wave_id = Column(String(250), primary_key=True)
    dashboard_name = Column(String(250))
    dashboard_type = Column(String(250))
    display_name = Column(String(250))
    url = Column(String(250))
    link_var = Column(String(250))
    group_name = Column(String(250))
    folder_id = Column(String(250))
    env = Column(String(250))
    pages = relationship("AssociationEntity", back_populates="dashboard")

    def __init__(self, wave_id=None, dashboard_name='', dashboard_type='', display_name='', url='', link_var='',
                 group_name='', folder_id='', env='', pages=[]):
        self.wave_id = wave_id
        self.dashboard_name = dashboard_name
        self.dashboard_type = dashboard_type
        self.display_name = display_name
        self.url = url
        self.link_var = link_var
        self.group_name = group_name
        self.folder_id = folder_id
        self.env = env
        self.pages = pages


class DatasetEntity(EntityBase):
    __schema__ = 'dashboard_ui'
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    type = Column(String(250))
    name = Column(String(250))
    env = Column(String(250))

    def __init__(self, id=None, type='', name='', env=''):
        self.id = id
        self.type = type
        self.name = name
        self.env = env

