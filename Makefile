.PHONY: run

run:
	docker-compose -f deployments/docker/docker-compose.yml up --build

migrate:
	python django_app/manage.py migrate

createsuper:
	python django_app/manage.py createsuperuser

lint:
	ruff check src django_app

test:
	pytest

install-dev:
	python -m pip install --upgrade pip; \
	python -m pip install -r requirements-dev.txt
