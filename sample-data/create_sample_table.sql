
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


