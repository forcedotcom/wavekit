/**
  Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FIT
 */
drop schema test_data cascade;

create schema test_data;

create table test_data.demographic(
    year integer,
    REGION varchar(20),
    STATE varchar(20),
    CENSUS2010POP integer,
    DOMESTICMIG integer,
    POPESTIMATE integer,
    DEATHS integer,
    BIRTHS integer,
    INTERNATIONALMIG integer,
    ESTIMATESBASE integer,
    NATURALINC integer
);


