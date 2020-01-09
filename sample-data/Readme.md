
This sample data is created on postgres database. All scripts were tested on postgres. 

To create sample database, you need to run as a postgres user:
```
psql < create_db.sql
```

Run as test_user to create sample table(demographic):
```
psql -U test_user testdb < create_sample_table.sql
```

Run below script as postgres user to load data, you have run the command on your database host. 
```
./load_data.sh

# or run as a postgres user 
COPY test_data.demographic (year,DOMESTICMIG,REGION,CENSUS2010POP,STATE,POPESTIMATE,BIRTHS,NATURALINC,INTERNATIONALMIG,DEATHS,ESTIMATESBASE)
 FROM '${PWD}/us_demographic.csv' DELIMITER ',' CSV HEADER;;
```