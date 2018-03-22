.PHONY: test clean install publish test-publish sign

TP_FILES := setup.py setup.cfg widdy Makefile LICENSE.txt README.md
DIST     := transpiled/dist
PY       := 3
PYTHON   = python$(PY)

all: clean test

test: $(TP_FILES)
	python3 -m flake8
	pytest-3 -s widdy
	$(PYTHON) -m widdy.demos --help >/dev/null

clean:
	pyclean .
	rm -rf .cache dist build ohlcwid.egg-info

install: $(TP_FILES)
	# Directly install widdy in the local system. This will link your installation
	# to the code in this repo for quick and easy local development.
	pip3 install --user -e .

transpiled: $(TP_FILES)
	mkdir -p transpiled
	cp -r $(TP_FILES) transpiled
	pasteurize -w --no-diff transpiled/widdy
	$(MAKE) -C transpiled dist PY=2 DIST=dist
	ls $(DIST)

dist: test $(TP_FILES)
	rm -f $@/*.whl $@/*.asc
	python3 setup.py bdist_wheel

sign: $(DIST)
	gpg --detach-sign -a $(DIST)/*.whl

test-publish: test transpiled
	twine upload --repository testpypi $(DIST)/*

publish: test transpiled sign
	twine upload --repository pypi $(DIST)/*

docker-test:
	docker run -it python:$(PY) bash -i -c 'pip install widdy; widdy all; true'
