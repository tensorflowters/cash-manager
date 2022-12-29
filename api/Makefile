.PHONY: help

HOST = ${HOSTNAME}

help:
	@echo "cash_manager Projects"
	@echo "~~~~~~~~~~~~~~~"
	@echo ""
	@echo "check        : Health check"
	@echo "coverage     : Make test coverage"
	@echo "docup        : Run docker compose services"
	@echo "docdown      : Stop docker containers"
	@echo "migrations   : Make django migrations"
	@echo "install      : Install python requirements"
	@echo "recover      : docdown + docup + wait + migrations + loaddata"
	@echo "runserver    : Run django server in debug mode"
	@echo "run_gunicorn : Run django server with gunicorn"
	@echo "static       : Collect static files"
	@echo "superuser    : Create django super user"
	@echo "test         : Start django test runner"
	@echo "translation  : Translation operation"
	@echo "wait         : Wait for 3 seconds"
	@echo ""

check:
	@python manage.py check

coverage:
	@coverage run --source='../api' manage.py test
	@coverage report -m
	@coverage html
	@coverage xml

docup:
	@docker compose --env-file ./env up -d --build

docdown:
	@docker compose down -v

dumpdata:
	@python manage.py dumpdata -o dummy.json

loaddata:
	@python manage.py loaddata scripts/dummy.json

migration:
	@python manage.py makemigrations
	@python manage.py migrate

install:
	@pip3 install -r requirements.txt

recover: install docdown docup wait migration loaddata
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

recover_refactor: install docdown docup wait migration superuser
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

runserver:
	@python manage.py runserver ${HOST}:8000

run_gunicorn:
	@gunicorn cash_manager.wsgi:application --bind 0.0.0.0:8000 --daemon
	@nginx -g 'daemon off;'

collect:
	@python manage.py collectstatic --no-input

superuser:
	@python manage.py createsuperuser

tests:
	@python manage.py test

translation:
	@python manage.py makemessages -l tr
	@python manage.py compilemessages

wait:
	@sleep 3

runproxyversion:
	@make collect
	@make migration
	@make run_gunicorn