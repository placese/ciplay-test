CREATE DATABASE ciplay;

create user test with encrypted password 'test';

grant all privileges on database ciplay to test;

\c ciplay

psql -h localhost -p 5432 postgres

CREATE TABLE statistics (
  date DATE PRIMARY KEY,
  views INT,
  clicks INT,
  cost FLOAT
);
