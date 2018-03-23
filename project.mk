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
#
# New Project Quickstart 
# ----------------------
# Just run `make clone PREFIX=path/to NEW_PRJ=new_project
# This will copy all important files to $(PREFIX)/$(NEW_PRJ)
# and try to replace all relevant old $(PRJ) strings with $(NEW_PRJ)
#
# Notes
# -----
# All _lower_case vars are internal vars not supposed to be overwritten
#

.PHONY: all test base-test clean install publish test-publish sign docker-test docker-base-test clone

# The default project name is the name of the current dir
PRJ      := $(shell basename $(CURDIR))
# All code should reside in another subdir with that name of the project
PRJ_FILES := setup.py setup.cfg project.cfg project.mk Makefile LICENSE.txt README.md
TP_FILES := $(PRJ) $(PRJ_FILES)
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

_prj_path  := $(PREFIX)/$(NEW_PRJ)
_prj_files := $(patsubst %,$(_prj_path)/%,$(PRJ_FILES))
clone:
	test -n "$(NEW_PRJ)" -a -n "$(PREFIX)"
	! test -e $(_prj_path)  # target project path must not exist
	mkdir -p $(_prj_path)
	cp $(PRJ_FILES) $(_prj_path)
	# replace all refs to current project with new project
	sed -i 's#$(PRJ)#$(NEW_PRJ)#g' $(_prj_files)
	diff --color $(_prj_path) . 2> /dev/null || true  # compare the copied files to the source files

# docker-test also runs basic import and run test
docker-test: docker-base-test
