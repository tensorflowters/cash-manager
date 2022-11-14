# Cash manager

The aim of this project is to build a distant payment system that can receive and execute orders issued by
a terminal app on your phone.
<p>&nbsp;</p>

## <strong>Docker set-up</strong>
### 1. Build containers
```bash
docker-compose -p cash_manager build --no-cache
```
### 2. Start containers
```bash
$ sudo apt update
```
<p>&nbsp;</p>

## <strong>Create a super user for Django admin</strong>
### 1. Create a superuser
You need to create a superuser in order to access the django admin page
```bash
docker-compose exec api_dev python manage.py createsuperuser
```
### 2. Login on http://127.0.0.1:8000/admin/login/
<p>&nbsp;</p>

## <strong>Exporting data from database for the next seed</strong>
### 
pg_dump -U <db_username> <db_name> -h <host> -t <table_name> > seed.sql
Host can be found with docker inspect <the_container_id> of the database
```bash
docker-compose exec db_dev pg_dump -U postgres postgres -h 172.22.0.2 > seed.sql
```

