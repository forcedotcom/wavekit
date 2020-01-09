
create database testdb;

create user test_user with password 'test1';

GRANT CONNECT ON DATABASE testdb TO test_user;
grant all PRIVILEGES on database testdb to test_user;

