.PHONY: docker-test

MAIN := widdy
override PY ?= 3

include project.mk

docker-test:
	docker run -it python:$(PY) bash -i -c 'pip install widdy; widdy all; true'
