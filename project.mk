# Generic Project Makefile
# ========================
# Copy this file to each of python project to be able to test,
# build, and publish it easily.
#
# (c) Uwe Jugel, @ubunatic, License: MIT
#
# Integration and Usage
# ---------------------
# Simply `include project.mk` in your `Makefile`.
# Then add your common targets, such as `test`, `docker-test`, etc.
# Now use `make`, `make test`, `make install`, etc.
# See each target for more details.	

.PHONY: all test base-test clean install publish test-publish sign docker-test docker-base-test

# The default project name is the name of the current dir
PRJ      := $(shell basename $(CURDIR))
# All code should reside in another subdir with that name of the project
TP_FILES := $(PRJ) setup.py setup.cfg project.cfg project.mk Makefile LICENSE.txt README.md
# All code is assumed to be written for Py3, for Py2 support we need to transpile it
DIST     := transpiled/dist

# you can override, e.g., PY=2m to test other python versions
PY          = 3
PYTHON      = python$(PY)
# The main module is a module with the name of the project in the project subdir
MAIN        = $(PRJ).$(PRJ)
# Default tests include importing and running the module
CLI_TEST    = $(PYTHON) -m $(MAIN) -h >/dev/null
IMPORT_TEST = $(PYTHON) -c "import $(MAIN)"

all: clean test

# make test deend on base-test to trigger all tests
# when running `make test` (don't forget you write you own `test`!)
test: base-test

base-test: $(TP_FILES)
	# lint and test the project
	python3 -m flake8
	pytest-3 -s $(PRJ)
	$(CLI_TEST)
	$(IMPORT_TEST)

clean:
	pyclean .
	rm -rf .cache dist build transpiled $(PRJ).egg-info

install: $(TP_FILES)
	# Directly install $(PRJ) in the local system. This will link your installation
	# to the code in this repo for quick and easy local development.
	pip install --user -e .

transpiled: $(TP_FILES)
	# copy all code to transpiled, try to convert it to Py2, and build the dist there
	mkdir -p transpiled
	cp -r $(TP_FILES) transpiled
	pasteurize -w --no-diff transpiled/$(PRJ)
	$(MAKE) -C transpiled dist PY=2 DIST=dist PRJ=$(PRJ)
	ls $(DIST)

dist: test $(TP_FILES)
	# build the dist (should be called via transpiled)
	rm -f $@/*.whl $@/*.asc
	python3 setup.py bdist_wheel

sign: $(DIST)
	# sign the dist with your gpg key
	gpg --detach-sign -a $(DIST)/*.whl

test-publish: test transpiled
	# upload to testpypi (need valid ~/.pypirc)
	twine upload --repository testpypi $(DIST)/*

publish: test transpiled sign
	# upload to pypi (requires pypi account)
	twine upload --repository pypi $(DIST)/*

docker-base-test:
	# after pushing to pypi you want to check if you can pull and run
	# in a clean environment. Safest bet is to use docker!
	docker run -it python:$(PY) bash -i -c 'pip install $(PRJ); $(IMPORT_TEST); $(CLI_TEST)'

# docker-test also runs basic import and run test
docker-test: docker-base-test
