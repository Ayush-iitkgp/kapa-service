default: help

help:
	@echo "make format"
	@echo "make run"
	@echo "make migrate"
	@echo "make create-migration"
	@echo "make create-superuser"
	@echo "make create-cachetable"
	@echo "make bootstrap"

format:
	isort root org query utils
	black root org query utils

run:
	python manage.py runserver 0.0.0.0:8002

migrate:
	python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

create-migration:
	python manage.py makemigrations

create-superuser:
	python manage.py createsuperuser

create-cachetable:
	python manage.py createcachetable 	

bootstrap:
	make migrate org && make migrate && make create-cachetable