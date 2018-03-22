.PHONY: test docker-demos

include project.mk

test: $(TP_FILES)
	$(PYTHON) -m widdy.demos --help >/dev/null

docker-test:
	docker run -it python:$(PY) bash -i -c 'pip install widdy; widdy all; true'
