.PHONY: test docker-demos

MAIN := widdy.demos

include project.mk

test: $(TP_FILES)
	$(PYTHON) -m $(MAIN) --help >/dev/null

docker-test:
	docker run -it python:$(PY) bash -i -c 'pip install widdy; widdy all; true'
