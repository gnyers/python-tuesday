drop database if exists pydb;
drop user if exists pyuser;


create user pyuser identified by 'password';

create database pydb;
grant all on pydb.* to 'pyuser'@'%';
flush privileges;

show grants for pyuser;
