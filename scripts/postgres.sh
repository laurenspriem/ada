#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE account;
	CREATE DATABASE bidding;
	CREATE DATABASE communication;
	CREATE DATABASE marketplace;
	CREATE DATABASE picture;
EOSQL
