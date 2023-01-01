buildserver:
	@docker compose --env-file .env up -d --build

downserver:
	@docker compose stop
	@docker compose down -v

buildprod:
	@docker-compose -f docker-compose.prod.local.yml --env-file .env.prod.local build --no-cache
	@docker-compose -f docker-compose.prod.local.yml --env-file .env.prod.local up -d

downprod:
	@docker compose stop
	@docker-compose -f docker-compose.prod.local.yml down -v

builddev:
	@docker-compose -f docker-compose.dev.yml up -d --build

downdev:
	@docker-compose -f docker-compose.dev.yml down -v

migration:
	@python manage.py makemigrations
	@python manage.py migrate

install:
	@pip3 install -r requirements.txt

recover_refactor: install docdown docup wait migration superuser
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

runserver:
	@python manage.py runserver ${HOST}:8000

run_gunicorn:
	@gunicorn cash_manager.wsgi:application --bind 0.0.0.0:8000

collect:
	@python manage.py collectstatic --no-input

translation:
	@python manage.py makemessages -l tr
	@python manage.py compilemessages

wait:
	@sleep 3

runproxyversion:
	@make collect
	@make migration
	@make run_gunicorn
