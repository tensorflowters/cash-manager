#! /bin/bash

CONTAINER_NAME=cash_manager_database

docker container run --name $CONTAINER_NAME_dev -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -v postgres_dev:/var/lib/postgresql/data -d postgres