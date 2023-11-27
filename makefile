ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif

dc up:
	docker compose up -d

dc down:
	docker compose down

dc down-v:
	docker compose down -v

dc build:
	docker compose up --build -d --remove-orphans

dc logs:
	docker compose logs

dvi:
	docker volume inspect rentit_postgres_data

djmm:
	docker compose exec api python manage.py makemigrations

djm:
	docker compose exec api python manage.py migrate

djs:
	docker compose exec api python manage.py shell

djc:
	docker compose exec api -it api /bin/bash

create_su:
	docker compose exec api python manage.py createsuperuser

collectstatic:
	docker compose exec api python manage.py collectstatic --no-input --clear

rentit-db:
	docker compose exec postgres-db psql --username=postgres --dbname=rent

test:
	docker compose exec api pytest -p no:warnings --cov=.
