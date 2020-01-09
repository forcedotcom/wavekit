/**
This file contains sql script to create metadata model
**/
drop schema if exists dashboard_ui cascade;
create schema dashboard_ui;

create table dashboard_ui.dataset (
   id serial,
   type varchar,
   name varchar,
   env varchar,
   constraint dashboard_ui_dataset_pk primary key (name)
);

create table dashboard_ui.dashboard (
   dashboard_name varchar not null,
   display_name varchar not null,
   wave_id varchar,
   url varchar,
   link_var varchar,
   dashboard_type varchar,
   group_name varchar,
   folder_id varchar,
   env varchar,
   constraint dashboard_ui_dashboard_pk primary key (dashboard_name)
);

create table dashboard_ui.page (
    name varchar not null,
    display_name varchar,
    template_file varchar,
    constraint dashboard_ui_page_pk primary key (name)
);

create table dashboard_ui.container_widget (
    name varchar not null,
    display_name varchar,
    template_file varchar,
    page_name varchar references dashboard_ui.page(name),
    colspan integer,
    col integer,
    row integer,
    rowspan integer,
    constraint dashboard_ui_container_widget_pk primary key (name)
);

create table dashboard_ui.page_dashboard_relationship (
    dashboard_name varchar not null references dashboard_ui.dashboard(dashboard_name),
    page_name varchar not null references dashboard_ui.page(name)
);

create table dashboard_ui.widgets (
   name varchar not null,
   display_name varchar,
   container_name varchar references dashboard_ui.container_widget(name),
   font_size integer,
   template_file varchar,
   type varchar,
   colspan integer,
   col integer,
   row integer,
   rowspan integer,
   constraint dashboard_ui_widget_pk primary key (name)
);

create table dashboard_ui.widget_property (
    id serial,
    widget_name varchar references dashboard_ui.widgets(name),
    key varchar,
    value varchar,
    constraint dashboard_ui_widget_property primary key (id)
);

create table dashboard_ui.steps (
    name varchar not null,
    display_name varchar,
    widget_name varchar references dashboard_ui.widgets(name),
    type varchar,
    template_file varchar,
    constraint dashboard_ui_steps primary key (name)
);

create table dashboard_ui.step_property (
    id serial,
    step_name varchar references dashboard_ui.steps(name),
    key varchar,
    value varchar,
    constraint dashboard_ui_step_property primary key (id)
);