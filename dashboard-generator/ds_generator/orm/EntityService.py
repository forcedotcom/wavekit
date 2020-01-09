"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from sqlalchemy import create_engine, Table, Column
from sqlalchemy.orm import sessionmaker

from ds_generator.Models import Property, Step, Widget, Container, Dashboard, Dataset, Page
from .EntityModels import EntityBase, StepEntity, StepPropertyEntity, WidgetEntity, WidgetPropertyEntity, \
    ContainerEntity, DashboardEntity, DatasetEntity, AssociationEntity, PageEntity


class EntityService:
    def __init__(self, config=None):
        if config is None:
            self.engineName = 'sqlite'
            self.engine = create_engine('sqlite:///:memory:')
            EntityBase.metadata.bind = self.engine
            self.session = self.mkSession()
        else:
            self.engineName = 'postgresql'
            #print 'postgresql://' + config.username + ':' + config.password + '@'+  config.host+':5432/' + config.database
            self.engine = create_engine('postgresql+pygresql://' + config.username + ':' + config.password + '@'+  config.host+':5432/' + config.database)
            EntityBase.metadata.bind = self.engine
            self.session = self.mkSession(config.schema)

    def mkSession(self, schema=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        if 'postgresql' in self.engineName:
            session.execute('SET search_path to ' + schema)
        return session

    def add_property_to_step(self, property, step_name):
        """
        Method adds provided Property to a Step by name and inserts Property into 'step_property' table as
        StepPropertyEntity
        :param property:
        :param step_name:
        :return:
        """
        step_property_entity = StepPropertyEntity(step_name=step_name,
                                                  key=property.get_key(),
                                                  value=property.get_value())
        self.session.add(step_property_entity)
        self.session.commit()
        property.id = step_property_entity.id

    def get_step_properties(self, step_name):
        """
        Method returns list of Properties belonging to the provided Step
        :param step_name:
        :return step_properties:
        """
        step_property_list = self.session.query(StepPropertyEntity).filter_by(step_name=step_name).all()
        step_properties = []
        for sp in step_property_list:
            step_properties.append(Property(sp.id, sp.key, sp.value))
        return step_properties

    def add_property_to_widget(self, property, widget_name):
        """
        Method adds provided Property to a Widget by name and inserts Property into 'widget_property' table as
        WidgetPropertyEntity
        :param property:
        :param widget_name:
        :return:
        """
        widget_property_entity = WidgetPropertyEntity(widget_name=widget_name,
                                                      key=property.get_key(),
                                                      value=property.get_value())
        self.session.add(widget_property_entity)
        self.session.commit()
        property.id = widget_property_entity.id

    def add_step_to_widget(self, step, widget_name):
        """
        Method adds provided Step to a Widget by name and inserts Step into 'steps' table as StepEntity
        :param step:
        :param widget_name:
        :return:
        """
        step_entity = StepEntity(name=step.get_name(),
                                 widget_name=widget_name,
                                 display_name=step.get_display_name(),
                                 type=step.get_type(),
                                 template_file=step.get_template())
        self.session.add(step_entity)
        self.session.commit()

    def get_widget_properties(self, widget_name):
        """
        Method returns list of Properties belonging to provided Widget
        :param widget_name:
        :return widget_properties:
        """
        widget_property_list = self.session.query(WidgetPropertyEntity).filter_by(widget_name=widget_name).all()
        widget_properties = []
        for wp in widget_property_list:
            widget_properties.append(Property(wp.id, wp.key, wp.value))
        return widget_properties

    def get_widget_steps(self, widget_name):
        """
        Method returns list of Steps belonging to provided Widget
        :param widget_name:
        :return widget_steps:
        """
        widget_steps_list = self.session.query(StepEntity).filter_by(widget_name=widget_name).all()
        widget_steps = []
        for ws in widget_steps_list:
            widget_steps.append(Step(ws.name, ws.display_name, ws.type, ws.template_file))
        return widget_steps

    def add_widget_to_container(self, widget, container_name):
        """
        Method adds provided Widget to a Container by name and inserts Widget into 'widgets' table as WidgetEntity
        :param widget:
        :param container_name:
        :return:
        """
        widget_entity = WidgetEntity(name=widget.get_name(),
                                     display_name=widget.get_display_name(),
                                     container_name=container_name,
                                     font_size=widget.get_font_size(),
                                     template_file=widget.get_template(),
                                     type=widget.get_type(),
                                     colspan=widget.get_colspan(),
                                     col=widget.get_column(),
                                     row=widget.get_row(),
                                     rowspan=widget.get_rowspan())
        self.session.add(widget_entity)
        self.session.commit()

    def get_container_widgets(self, container_name):
        """
        Method returns list of Widgets belonging to provided Container
        :param container_name:
        :return widgets:
        """
        widget_list = self.session.query(WidgetEntity).filter_by(container_name=container_name).all()
        widgets = []
        for we in widget_list:
            widgets.append(Widget(we.name, we.display_name, we.font_size, we.template_file, we.type, we.colspan, we.col,
                                  we.row, we.rowspan))
        return widgets

    def add_container_to_page(self, container, page_name):
        """
        Method adds provided Container to a Page by name and inserts Container into 'containers' table as ContainerEntity
        :param container:
        :param page_name:
        :return:
        """
        container_entity = ContainerEntity(name=container.get_name(),
                                           display_name=container.get_display_name(),
                                           template_file=container.get_template(),
                                           page_name=page_name,
                                           colspan=container.get_colspan(),
                                           col=container.get_column(),
                                           row=container.get_row(),
                                           rowspan=container.get_rowspan())
        self.session.add(container_entity)
        self.session.commit()

    def get_page_containers(self, page_name):
        """
        Method returns list of Containers belonging to provided Page
        :param page_name:
        :return widgets:
        """
        container_list = self.session.query(ContainerEntity).filter_by(page_name=page_name).all()
        containers = []
        for ce in container_list:
            containers.append(Container(ce.name, ce.display_name, ce.template_file, ce.colspan, ce.col, ce.row,
                                        ce.rowspan))
        return containers

    def add_page(self, page):
        """
        Method inserts provided Page into 'pages' table as PageEntity
        :param page:
        :return:
        """
        page_entity = PageEntity(name=page.get_name(),
                                 display_name=page.get_display_name(),
                                 template_file=page.get_template())
        self.session.add(page_entity)
        self.session.commit()

    def get_dashboard_pages(self, dashboard_name):
        """
        Method returns list of Pages belonging to provided Dashboard
        :param dashboard_id:
        :return pages:
        """
        page_names = self.session.query(AssociationEntity).filter_by(dashboard_name=dashboard_name).all()
        pages = []
        for name in page_names:
            pe = self.session.query(PageEntity).filter_by(name=name.page_name).one()
            pages.append(Page(pe.name, pe.display_name, pe.template_file))
        return pages

    def get_dashboards_by_env(self, env):
        """
        Method returns list of Dashboards belonging to provided environment
        :param env:
        :return dashboards:
        """
        dashboard_entity_list = self.session.query(DashboardEntity).all()
        dashboards = []
        for de in dashboard_entity_list:
            if de.env == env:
                dashboards.append(
                    Dashboard(de.wave_id, de.dashboard_name, de.dashboard_type, de.display_name, de.url, de.link_var,
                              de.group_name, de.folder_id, de.env))
        return dashboards

    def add_new_dashboard(self, dashboard):
        """
        Method inserts provided Dashboard into 'dashboards' table as DashboardEntity
        :param dashboard:
        :return:
        """
        dashboard_entity = DashboardEntity(wave_id=dashboard.get_wave_id(),
                                           dashboard_name=dashboard.get_dashboard_name(),
                                           dashboard_type=dashboard.get_dashboard_type(),
                                           display_name=dashboard.get_display_name(),
                                           url=dashboard.get_url(),
                                           link_var=dashboard.get_link_var(),
                                           group_name=dashboard.get_group_name(),
                                           folder_id = dashboard.get_folder_id(),
                                           env=dashboard.get_env())
        self.session.add(dashboard_entity)
        self.session.commit()

    def get_dashboard_by_name(self, ds_name):
        """
        Method returns Dashboard that corresponds to provided wave ID
        :param dashboard_id:
        :return Dashboard:
        """
        d = self.session.query(DashboardEntity).filter_by(dashboard_name=ds_name).one()
        dashboard = Dashboard(d.wave_id, d.dashboard_name, d.dashboard_type, d.display_name, d.url, d.link_var,
                              d.group_name, d.folder_id, d.env)
        return dashboard

    def delete_dashboard_by_name(self, ds_name):
        """
        Method deletes provided Dashboard from 'dashboards' table
        :param wave_id:
        :return:
        """
        dashboard = self.session.query(DashboardEntity).filter_by(dashboard_name=ds_name).one()
        self.session.delete(dashboard)
        self.session.commit()

    def add_dataset(self, dataset):
        """
        Method inserts provided Dataset into 'dataset' table as DatasetEntity
        :param dataset:
        :return:
        """
        dataset_entity = DatasetEntity(type=dataset.get_type(),
                                       name=dataset.get_name(),
                                       env=dataset.get_env())
        self.session.add(dataset_entity)
        self.session.commit()

    def get_datasets_by_env(self, env):
        """
        Method returns list of Datasets belonging to provided environment
        :param env:
        :return datasets:
        """
        dataset_entity_list = self.session.query(DatasetEntity).all()
        datasets = []
        for ds in dataset_entity_list:
            if ds.env == env:
                datasets.append(
                    Dataset(ds.id, ds.type, ds.name, ds.env)
                )
        return datasets

    def add_relationship(self, dashboard_name, page_name):
        """
        Method adds relationship between provided Dashboard and Page and inserts the association into
        'page_dashboard_relationship' table as AssociationEntity
        :param dashboard_name:
        :param page_name:
        :return:
        """
        relationship_table = AssociationEntity(dashboard_name=dashboard_name,
                                               page_name=page_name)
        self.session.add(relationship_table)
        self.session.commit()

    def delete_relationship_by_name(self, dashboard_name, page_name):
        """
        Method deletes relationship between provided Dashboard and Page from 'page_dashboard_relationship'
        table
        :param dashboard_id:
        :param page_name:
        :return:
        """
        relationships = self.session.query(AssociationEntity).filter_by(dashboard_name=dashboard_name, page_name=page_name).one()
        self.session.delete(relationships)
        self.session.commit()

    def save_dashboard(self, dashboard):
        """
        save dashboard into database
        :param dashboard: dashboard object
        :return: None
        """
        ds_entity = self.session.query(DashboardEntity).filter_by(dashboard_name=dashboard.dashboard_name).one()
        ds_entity.wave_id = dashboard.get_wave_id()
        ds_entity.url = dashboard.url
        self.session.add(ds_entity)
        self.session.commit()