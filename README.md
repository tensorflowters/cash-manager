# Cash manager

The aim of this project is to build a distant payment system that can receive and execute orders issued by
a terminal app on your phone.
<p>&nbsp;</p>

## <strong>Docker set-up for local development</strong>
### 1. Build containers
```bash
docker-compose -f docker-compose.local.yml -p cash_manager build --no-cache
```
<p>&nbsp;</p>

### 2. Start containers
```bash
docker-compose -f docker-compose.local.yml -p cash_manager up -d
```
<p>&nbsp;</p>

### 3. Create a superuser
You need to create a superuser in order to access the django admin page
```bash
docker-compose -f docker-compose.local.yml -p cash_manager exec api_dev python manage.py createsuperuser
```
```bash
docker-compose -f docker-compose.local.yml -p cash_manager exec api_dev python manage.py changepassword superadmin
```
<p>&nbsp;</p>

### 4. Exporting data from database for the next seed
Login on http://127.0.0.1:8000/admin/login/
<p>&nbsp;</p>

pg_dump -U <db_username> <db_name> -h <host> -t <table_name> > seed.sql
Host can be found with docker inspect <the_container_id> of the database
<p>&nbsp;</p>

```bash
docker-compose -f docker-compose.local.yml -p cash_manager exec db_dev pg_dump -U postgres postgres -h 172.27.0.2 > seed.sql
```

<p>&nbsp;</p>

### 5. Make migrations
```bash
docker-compose -f docker-compose.local.yml -p cash_manager exec api_dev python manage.py makemigrations
```
<p>&nbsp;</p>

### 6. Migrate
```bash
docker-compose -f docker-compose.local.yml -p cash_manager exec api_dev python manage.py migrate
```
<p>&nbsp;</p>
