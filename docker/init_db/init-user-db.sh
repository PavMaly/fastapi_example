#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" -d "postgres"<<-EOSQL
	CREATE USER app;
	CREATE DATABASE app;
	GRANT ALL PRIVILEGES ON DATABASE app TO app;
	\c app
	GRANT ALL ON schema public TO app;
EOSQL