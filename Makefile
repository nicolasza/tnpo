.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")



.PHONY: venv
venv:			## Create a virtual environment
	@echo "Creating virtualenv ..."
	@rm -rf .venv
	@python3.12 -m pip install --user virtualenv
	@python3.12 -m virtualenv .venv
	@./.venv/bin/pip install -U pip
	@echo
	@echo "Run 'source .venv/bin/activate' to enable the environment"

.PHONY: install
install:
	pip install -r requirements.txt
	pip install -r requirements_dev.txt


.PHONY: run
run:
	uvicorn tnpo:application --host 0.0.0.0 --port 8080


.PHONY: model-test
model-test:			## Corre test de modelo
	mkdir reports || true
	pytest --junitxml=reports/report.xml  tests/model

.PHONY: api-test
api-test:			## corre test de api local
	mkdir reports || true
	pytest --junitxml=reports/report.xml tests/api 


.PHONY: build
build:
	docker build -t doubleit-api .

.PHONY: docker_run
docker_run:
	docker run -p 8080:8080 doubleit-api
