#!/usr/bin/env bash
export DATABASE_URL=postgresql://pguser:pgpass@localhost:5433/pgdb
make install && psql -a -d $DATABASE_URL -f database.sql


