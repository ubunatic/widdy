.PHONY: docker-test

MAIN   := widdy
PYTHON := python

include project.mk

docker-test:
	docker run -it python:$(PY) bash -i -c 'pip install widdy; widdy all; true'
