/** create data schema  */
create schema test_data;
grant all on all tables in schema test_data to test_user;
alter schema test_data owner to test_user;

/** create staging schema */
create schema dashboard_ui_prod;
grant all on all tables in schema dashboard_ui_prod to test_user;
alter schema dashboard_ui_prod owner to test_user;

/** create production schema */
create schema dashboard_ui_staging;
grant all on all tables in schema dashboard_ui_staging to test_user;
alter schema dashboard_ui_staging owner to test_user;