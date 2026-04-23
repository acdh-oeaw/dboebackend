#!/bin/bash

pg_dump -d dboebackend -h localhost -p 5433 -U  dboebackend -c -f dboebackend_dump1.sql
# psql -U postgres -d dboeplay < dboebackend_dump1.sql


# pg_dump -d dboeannotation_prod -h localhost -p 5433 -U  dboeannotation_prod -c -f dboeannotation_prod_dump.sql
# psql -U postgres -d dboeannotation_prod < dboeannotation_prod_dump.sql
