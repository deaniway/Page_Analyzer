#!/usr/bin/env bash
docker exec -i dev_page_analyzer psql -U pguser -d pgdb -f database.sql


