.PHONY: help install clean docker-push docker-build

.DEFAULT_GOAL := help
SHELL := /bin/bash
PATH := ${PWD}/venv/bin:${PATH}
PYTHONPATH := ${PWD}:${PYTHONPATH}

export

BOLD=$(shell tput -T xterm bold)
RED=$(shell tput -T xterm setaf 1)
GREEN=$(shell tput -T xterm setaf 2)
YELLOW=$(shell tput -T xterm setaf 3)
RESET=$(shell tput -T xterm sgr0)


include .env

help:
	@awk 'BEGIN {FS = ":.*?##-.*?local.*?- "} /^[a-zA-Z_-]+:.*?##-.*?local.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "${YELLOW}ENV=data${RESET}"
	@awk 'BEGIN {FS = ":.*?##-.*?data.*?- "} /^[a-zA-Z_-]+:.*?##-.*?data.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "${YELLOW}ENV=sandbox${RESET}"
	@awk 'BEGIN {FS = ":.*?##-.*?sandbox.*?- "} /^[a-zA-Z_-]+:.*?##-.*?sandbox.*?- / \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ##-local- Setup project
install: clean
	virtualenv -p python3.7 venv
	pip3 install -r requirements.txt

install-geo: install
	pip3 install -r requirements-geo.txt

install-prophet: install
	pip3 install -r requirements-prophet.txt

install-auto-arima: install
	pip3 install -r requirements-auto-arima.txt

install-all: install install-auto-arima install-geo install-prophet


clean: ##-local- Cleanup project
	rm -rf venv

# -------------------------------------------------------------------
# DOCKER
# -------------------------------------------------------------------

docker-build:  ##-local- Build image
docker-build:
	docker build -t scikit-hts-examples:${HTS_VERSION} .
	docker tag scikit-hts-examples:${HTS_VERSION} carlomazzaferro/scikit-hts-examples:${HTS_VERSION}

docker-run:
	docker run -p 8000:8888 -it scikit-hts-examples:${HTS_VERSION} .

docker-push:  ##-sandbox- Build & push image to Dockerhub
docker-push: docker-build
	docker push carlomazzaferro/scikit-hts-examples:${HTS_VERSION}
