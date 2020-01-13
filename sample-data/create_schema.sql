/**
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FIT
 */
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