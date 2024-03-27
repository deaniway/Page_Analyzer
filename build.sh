#!/usr/bin/env bash
export DATABASE_URL=postgresql://pguser:pgpass@localhost:5433/pgdb
make install && docker exec -it dev_page_analyzer psql -U pguser -d pgdb psql
