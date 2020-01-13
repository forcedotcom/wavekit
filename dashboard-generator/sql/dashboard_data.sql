/**
  Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FIT
 */
-- Datasets --
insert into dashboard_ui.dataset values(default, '1p_period', 'period1', 'sandbox');
insert into dashboard_ui.dataset values(default, '1p_breakdown', 'breakdown_type1', 'sandbox');
insert into dashboard_ui.dataset values(default, 'yearly_demo_1', 'yearly_demo_1', 'sandbox');
insert into dashboard_ui.dataset values(default, '1p_sort_order', 'sort_order', 'sandbox');
insert into dashboard_ui.dataset values(default, '1p_sort_type', 'sort_type', 'sandbox');

-- DASHBOARDS --
insert into dashboard_ui.dashboard values('ds1', 'Sample Cost Analytics', '0FK0u0000000166GAA', '/services/data/v46.0/wave/dashboards/0FK0u0000000166GAA',
                                    'link_var', 'dashboard_type', 'group_name', '00l0u000000DnVMAA0','sandbox');

-- PAGES --
insert into dashboard_ui.page values('_total_infra_cost_page', 'Total Infra Cost', 'page_template.json');


-- title --
insert into dashboard_ui.container_widget values('title_container_1p', 'Dashboard title', 'container_widget.json', '_total_infra_cost_page', 37, 0, 0, 1);


insert into dashboard_ui.widgets values('sample_cost_analytics_text_1p', '', 'title_container_1p', 12, 'text_widget.json', 'static_text', 37, 0, 0, 1);
insert into dashboard_ui.widget_property values(default, 'sample_cost_analytics_text_1p', 'text', 'Sample Analytics > Census > United States');
insert into dashboard_ui.widget_property values(default, 'sample_cost_analytics_text_1p', 'text_colour', '#FFFFFF');
insert into dashboard_ui.widget_property values(default, 'sample_cost_analytics_text_1p', 'alignment', 'left');
insert into dashboard_ui.widget_property values(default, 'sample_cost_analytics_text_1p', 'style', '"backgroundColor": "#091A3E","borderEdges": ["bottom"]');



-- DROPDOWN SECTION --
insert into dashboard_ui.container_widget values('filter_container_1p', 'Dropdown container', 'container_widget.json', '_total_infra_cost_page', 4, 33, 1, 3);

insert into dashboard_ui.widgets values('region_listselector_widget_1p', 'Region', 'filter_container_1p', 0, 'listselector_widget.json', 'listselector', 4, 33, 2, 1);
insert into dashboard_ui.steps values('Region_1', 'Region 1', 'region_listselector_widget_1p', '', '1P_listselector_step.json');
insert into dashboard_ui.step_property values(default, 'Region_1', 'group_name', 'region');
insert into dashboard_ui.step_property values(default, 'Region_1', 'saql_name', 'listselector_step.saql');
insert into dashboard_ui.step_property values(default, 'Region_1', 'select_mode', 'multi');

insert into dashboard_ui.widgets values('state_listselector_widget_1p', 'State', 'filter_container_1p', 0, 'listselector_widget.json', 'listselector', 4, 33, 3, 1);
insert into dashboard_ui.steps values('State_1', 'State 1', 'state_listselector_widget_1p', '', '1P_listselector_step.json');
insert into dashboard_ui.step_property values(default, 'State_1', 'group_name', 'state');
insert into dashboard_ui.step_property values(default, 'State_1', 'saql_name', 'listselector_step.saql');
insert into dashboard_ui.step_property values(default, 'State_1', 'select_mode', 'multi');


insert into dashboard_ui.widgets values('period_listselector_widget_1p', 'Period', 'filter_container_1p', 0, 'listselector_widget.json', 'listselector', 4, 33, 1, 1);
insert into dashboard_ui.steps values('Period_3', 'Period 3', 'period_listselector_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'Period_3', 'saql_name', 'period_step_query.saql');
insert into dashboard_ui.step_property values(default, 'Period_3', 'select_mode', 'multi');


-- COST BUCKETS SECTION --

-- Text Headers --

insert into dashboard_ui.container_widget values('cost_container_1p', 'Cost buckets', 'container_widget.json', '_total_infra_cost_page', 28, 5, 1, 4);

insert into dashboard_ui.widgets values('pop_est_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 4, 8, 1, 1);
insert into dashboard_ui.widget_property values(default, 'pop_est_text_widget_1p', 'text', 'Population Estimate');
insert into dashboard_ui.widget_property values(default , 'pop_est_text_widget_1p', 'text_colour', '#335779');
insert into dashboard_ui.widget_property values(default, 'pop_est_text_widget_1p', 'alignment', 'center');

insert into dashboard_ui.widgets values('dom_mig_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 4, 13, 1, 1);
insert into dashboard_ui.widget_property values(default, 'dom_mig_text_widget_1p', 'text', 'Domestic Migration');
insert into dashboard_ui.widget_property values(default , 'dom_mig_text_widget_1p', 'text_colour', '#335779');
insert into dashboard_ui.widget_property values(default, 'dom_mig_text_widget_1p', 'alignment', 'center');

insert into dashboard_ui.widgets values('int_mig_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 5, 18, 1, 1);
insert into dashboard_ui.widget_property values(default, 'int_mig_text_widget_1p', 'text', 'International Migration');
insert into dashboard_ui.widget_property values(default , 'int_mig_text_widget_1p', 'text_colour', '#335779');
insert into dashboard_ui.widget_property values(default, 'int_mig_text_widget_1p', 'alignment', 'center');

insert into dashboard_ui.widgets values('birth_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 5, 23, 1, 1);
insert into dashboard_ui.widget_property values(default, 'birth_text_widget_1p', 'text', 'Birth');
insert into dashboard_ui.widget_property values(default , 'birth_text_widget_1p', 'text_colour', '#335779');
insert into dashboard_ui.widget_property values(default, 'birth_text_widget_1p', 'alignment', 'center');

insert into dashboard_ui.widgets values('death_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 5, 28, 1, 1);
insert into dashboard_ui.widget_property values(default, 'death_text_widget_1p', 'text', 'Death');
insert into dashboard_ui.widget_property values(default , 'death_text_widget_1p', 'text_colour', '#335779');
insert into dashboard_ui.widget_property values(default, 'death_text_widget_1p', 'alignment', 'center');

insert into dashboard_ui.widgets values('period_month_text_widget_1p', '', 'cost_container_1p', 16, 'text_widget.json', 'static_text', 3, 5, 1, 1);
insert into dashboard_ui.widget_property values(default, 'period_month_text_widget_1p', 'text', '{{cell(Period_3.selection, 0, \"Period\").asString()}}');
insert into dashboard_ui.widget_property values(default , 'period_month_text_widget_1p', 'text_colour', '#091A3E');
insert into dashboard_ui.widget_property values(default, 'period_month_text_widget_1p', 'alignment', 'left');

-- $$ values --

insert into dashboard_ui.widgets values('population_value_text_widget_1p', 'Population', 'cost_container_1p', 32, 'calculation_text_widget.json', 'dynamic_text', 4, 8, 2, 2);
insert into dashboard_ui.steps values('population_value_step_1p', '', 'population_value_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'population_value_step_1p', 'saql_name', 'population.saql');
insert into dashboard_ui.step_property values(default, 'population_value_step_1p', 'var_name', 'sum_value');

insert into dashboard_ui.widgets values('domestic_migration_value_text_widget_1p', 'Domestic Migration', 'cost_container_1p', 32, 'calculation_text_widget.json', 'dynamic_text', 4, 13, 2, 2);
insert into dashboard_ui.steps values('domestic_migration_value_step_1p', '', 'domestic_migration_value_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'domestic_migration_value_step_1p', 'saql_name', 'domestic_migration.saql');
insert into dashboard_ui.step_property values(default, 'domestic_migration_value_step_1p', 'var_name', 'sum_value');

insert into dashboard_ui.widgets values('international_migration_text_widget_1p', 'International Migration', 'cost_container_1p', 32, 'calculation_text_widget.json', 'dynamic_text', 5, 18, 2, 2);
insert into dashboard_ui.steps values('international_migration_value_step_1p', '', 'international_migration_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'international_migration_value_step_1p', 'saql_name', 'international_migration.saql');
insert into dashboard_ui.step_property values(default, 'international_migration_value_step_1p', 'var_name', 'sum_value');

insert into dashboard_ui.widgets values('birth_value_text_widget_1p', 'Birth', 'cost_container_1p', 32, 'calculation_text_widget.json', 'dynamic_text', 5, 23, 2, 2);
insert into dashboard_ui.steps values('birth_value_step_1p', '', 'birth_value_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'birth_value_step_1p', 'saql_name', 'birth.saql');
insert into dashboard_ui.step_property values(default, 'birth_value_step_1p', 'var_name', 'sum_value');

insert into dashboard_ui.widgets values('death_value_text_widget_1p', 'Death', 'cost_container_1p', 32, 'calculation_text_widget.json', 'dynamic_text', 5, 28, 2, 2);
insert into dashboard_ui.steps values('death_value_step_1p', '', 'death_value_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'death_value_step_1p', 'saql_name', 'death.saql');
insert into dashboard_ui.step_property values(default, 'death_value_step_1p', 'var_name', 'sum_value');

-- MoM --
insert into dashboard_ui.widgets values('population_mom_text_widget_1p', 'Population MoM', 'cost_container_1p', 16, 'calculation_text_widget.json', 'dynamic_text', 4, 8, 4, 1);
insert into dashboard_ui.steps values('population_mom_step_1p', '', 'population_mom_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'population_mom_step_1p', 'saql_name', 'population_mom.saql');
insert into dashboard_ui.step_property values(default, 'population_mom_step_1p', 'var_name', 'mom');

insert into dashboard_ui.widgets values('domestic_migration_mom_text_widget_1p', 'Domestic Migration MoM', 'cost_container_1p', 16, 'calculation_text_widget.json', 'dynamic_text', 4, 13, 4, 1);
insert into dashboard_ui.steps values('domestic_migration_mom_step_1p', '', 'domestic_migration_mom_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'domestic_migration_mom_step_1p', 'saql_name', 'domestic_migration_mom.saql');
insert into dashboard_ui.step_property values(default, 'domestic_migration_mom_step_1p', 'var_name', 'mom');

insert into dashboard_ui.widgets values('international_migration_mom_text_widget_1p', 'International Migration MoM', 'cost_container_1p', 16, 'calculation_text_widget.json', 'dynamic_text', 5, 18, 4, 1);
insert into dashboard_ui.steps values('international_migration_mom_step_1p', '', 'international_migration_mom_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'international_migration_mom_step_1p', 'saql_name', 'international_migration_mom.saql');
insert into dashboard_ui.step_property values(default, 'international_migration_mom_step_1p', 'var_name', 'mom');

insert into dashboard_ui.widgets values('birth_mom_text_widget_1p', 'Birth MoM', 'cost_container_1p', 16, 'calculation_text_widget.json', 'dynamic_text', 5, 23, 4, 1);
insert into dashboard_ui.steps values('birth_mom_step_1p', '', 'birth_mom_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'birth_mom_step_1p', 'saql_name', 'birth_mom.saql');
insert into dashboard_ui.step_property values(default, 'birth_mom_step_1p', 'var_name', 'mom');

insert into dashboard_ui.widgets values('death_mom_text_widget_1p', 'Death MoM', 'cost_container_1p', 16, 'calculation_text_widget.json', 'dynamic_text', 5, 28, 4, 1);
insert into dashboard_ui.steps values('death_mom_step_1p', '', 'death_mom_text_widget_1p', 'chart', 'chart_step.json');
insert into dashboard_ui.step_property values(default, 'death_mom_step_1p', 'saql_name', 'death_mom.saql');
insert into dashboard_ui.step_property values(default, 'death_mom_step_1p', 'var_name', 'mom');

-- SIDE LINKS SECTION --
insert into dashboard_ui.container_widget values('side_links_container_1p', 'Side links container', 'container_widget.json', '_total_infra_cost_page', 5, 0, 1, 15);


insert into dashboard_ui.widgets values('us_text_widget_1p', '', 'side_links_container_1p', 16, 'text_widget.json', 'static_text', 5, 0, 1, 1);
insert into dashboard_ui.widget_property values(default, 'us_text_widget_1p', 'text', 'United States');
insert into dashboard_ui.widget_property values(default , 'us_text_widget_1p', 'text_colour', 'rgb(1, 73, 157)');
insert into dashboard_ui.widget_property values(default, 'us_text_widget_1p', 'alignment', 'left');

insert into dashboard_ui.widgets values('canada_text_widget_1p', '', 'side_links_container_1p', 16, 'text_widget.json', 'static_text', 5, 0, 2, 1);
insert into dashboard_ui.widget_property values(default, 'canada_text_widget_1p', 'text', 'Canada');
insert into dashboard_ui.widget_property values(default, 'canada_text_widget_1p', 'text_colour', '#7d98b3');
insert into dashboard_ui.widget_property values(default, 'canada_text_widget_1p', 'alignment', 'left');

insert into dashboard_ui.widgets values('etc_text_widget_1p', '', 'side_links_container_1p', 16, 'text_widget.json', 'static_text', 5, 0, 3, 1);
insert into dashboard_ui.widget_property values(default, 'etc_text_widget_1p', 'text', 'Etc.');
insert into dashboard_ui.widget_property values(default, 'etc_text_widget_1p', 'text_colour', '#7d98b3');
insert into dashboard_ui.widget_property values(default, 'etc_text_widget_1p', 'alignment', 'left');



-- CHART #1 SECTION --

insert into dashboard_ui.container_widget values('chart_1_container_1p', 'Chart #1 section', 'container_widget.json', '_total_infra_cost_page', 28, 5, 5, 6);


insert into dashboard_ui.widgets values('population_chart_widget_1p', 'Population Region Series', 'chart_1_container_1p', 16, 'bar_chart_widget.json', 'bar_chart', 25, 8, 5, 6);
insert into dashboard_ui.steps values('Period_Year_Period_M_1', 'Period Year Period', 'population_chart_widget_1p', 'chart', 'chart_widget_step.json');
insert into dashboard_ui.step_property values(default, 'Period_Year_Period_M_1', 'saql_name', 'population_chart.saql');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'bins', '');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'axis_mode', 'sync');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'vis_type', 'stackvbar');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'chart_title', 'Annual Population by Region');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'title_1', 'Fully Burdened Infra Cost');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'title_2', ' ');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'show_title', true);
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'show_axis', true);
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'show_action', true);
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'show_legend', true);
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'col_map', '');
insert into dashboard_ui.widget_property values(default, 'population_chart_widget_1p', 'sum', 'absolute');




-- DASHBOARD owners Page  RELATIONSHIP --
insert into dashboard_ui.page_dashboard_relationship values('ds1', '_total_infra_cost_page');


