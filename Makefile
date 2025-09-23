.PHONY: run

run:
	docker-compose -f deployments/docker/docker-compose.yml up --build

migrate:
	python django_app/manage.py migrate

createsuper:
	python django_app/manage.py createsuperuser

lint:
	flake8 src django_app

test:
	pytest
