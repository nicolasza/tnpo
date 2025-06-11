.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install_dev
install_dev:
	pip install -r requirements_dev.txt


.PHONY: run
run:
	uvicorn tnpo:application --host 0.0.0.0 --port 8080

.PHONY: run_flask
run_flask:
	python inference.py


.PHONY: model-test
model-test:			## Run tests and coverage
	mkdir reports || true
	pytest --junitxml=reports/report.xml  tests/model

.PHONY: api-test
api-test:			## Run tests and coverage
	mkdir reports || true
	pytest --junitxml=reports/report.xml tests/api 


.PHONY: build
build:
	docker build -t doubleit-api .

.PHONY: docker_run
docker_run:
	docker run -p 8080:8080 doubleit-api
