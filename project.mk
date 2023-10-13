# Generic Project Makefile
# ========================
# Copy this file to a Python project for easy
# testing, building, and publishing.
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
# This will copy all important build files to $(PREFIX)/$(NEW_PRJ)
# and try to replace all relevant old $(PRJ) strings with $(NEW_PRJ)
#
# Notes
# -----
# - All `_lower_case` vars are internal vars not supposed to be overwritten.
# - Try NOT to change this file in your project, but instead handle all
#   customizations in your own `Makefile`.
#

# The default project name is the name of the current dir
PRJ       := $(shell basename $(CURDIR))
PRJ_TESTS := $(shell if test -e tests; then echo tests; fi)
PRJ_TOOLS := setup.py project.mk
PRJ_FILES := setup.cfg project.cfg Makefile LICENSE.txt README.md

# You can override, e.g., PY=2 to test other python versions
PYTHON      ?= python
PY          ?= $(shell $(PYTHON) -c 'import sys; print(sys.version_info.major)')
PIP         ?= $(PYTHON) -m pip
# The main module is a module with the name of the project in the project subdir
MAIN        ?= $(PRJ)
DIST        ?= dist
# Default tests include importing and running the module
CLI_TEST    = $(PYTHON) -m $(MAIN) -h >/dev/null
IMPORT_TEST = $(PYTHON) -c "import $(MAIN)"

export PYTHONPATH+=:.

# Common Targets
# ==============
.PHONY: all clean test base-test

all: clean test

# make test depends on base-test to trigger all tests
# when running `make test` (don't forget you write you own `test`!)
test: install-tools base-test

base-test:
	# lint and test the project (PYTHONPATH = $(PYTHONPATH))
	pyclean .
	$(PYTHON) -m flake8
	$(PYTHON) -m pytest -s $(PRJ) $(PRJ_TESTS)
	$(CLI_TEST)
	$(IMPORT_TEST)

clean:
	pyclean .
	rm -rf .pytest_cache .cache dist build $(PRJ).egg-info

# Install Targets
# ===============
.PHONY: install install-source install-tools

install-source: test
	# Directly install $(PRJ) in the local system. This will link your installation
	# to the code in this repo for quick and easy local development.
	$(PIP) install -e .
	#
	# Source Installation
	# -------------------
	$(PIP) show $(PRJ)

install: install-source

install-tools:
	# ensure tools are present
	@$(PIP) show pytest || $(PIP) install pytest
	@$(PIP) show flake8 || $(PIP) install flake8

# Packaging
# =========
.PHONY: dist sign test-publish publish docker-base-test docker-test

dist: test
	# build the dist
	rm -f $@/*.whl $@/*.asc
	python3 setup.py bdist_wheel

sign: $(DIST)
	# sign the dist with your gpg key
	gpg --detach-sign -a $(DIST)/*.whl

test-publish: test dist
	# upload to testpypi (need valid ~/.pypirc)
	twine check $(DIST)/*
	twine upload --repository testpypi $(DIST)/*

publish: test dist sign
	# upload to pypi (requires pypi account)
	twine upload --repository pypi $(DIST)/*

docker-base-test:
	# after pushing to pypi you want to check if you can pull and run
	# in a clean environment. Safest bet is to use docker!
	docker run -it python:$(PY) bash -i -c 'pip install $(PRJ); $(IMPORT_TEST); $(CLI_TEST)'

# docker-test also runs basic import and run test
docker-test: docker-base-test

# Project Clone Target
# --------------------
# The `clone` target copies all required files to a new dir and will setup a
# new Python project for you, in which you can use the same build features that
# `project.mk` provides for the current project.
#
_prj_path     := $(PREFIX)/$(NEW_PRJ)
_prj_main     := $(NEW_PRJ).$(NEW_PRJ)
_prj_tests    := $(_prj_path)/tests
_prj_package  := $(PREFIX)/$(NEW_PRJ)/$(NEW_PRJ)
_prj_files    := $(patsubst %,$(_prj_path)/%,$(PRJ_FILES))
_unsafe_clone := false
_diff         := 2> /dev/null diff --color
_expr_eq      := \([ ]*=[ ]*\).*
_expr_assig   := \(-m[ ]*\|:=[ ]*\|=[ ]*\)
_expr_sub     := $(PRJ)[a-z\.]\+
_prj_test     := $(_prj_tests)/test_$(NEW_PRJ).py
_prj_test_def := def test_$(NEW_PRJ)(): pass
_clone_files  := $(PRJ_FILES) .gitignore

.PHONY: check-project check-clone copy-tools merge-project clone-project

check-project:
	test -n "$(NEW_PRJ)" -a -n "$(PREFIX)"  # ensure that NEW_PRJ name and PREFIX path are set

check-clone: check-project
	! test -e $(_prj_path)                  # target project path must not exist

copy-tools: check-project
	mkdir -p $(_prj_path)                   # create project path
	cp -f $(PRJ_TOOLS) $(_prj_path)         # copy project tools that do not have any custom code/names

merge-project: copy-tools
	mkdir -p $(_prj_package) $(_prj_tests)  # create package path and tests path
	cp -r -n $(_clone_files) $(_prj_path)   # copy all project files (do not overwrite existing)
	sed -i 's#main$(_expr_eq)#main\1$(_prj_main)#g'        $(_prj_path)/project.cfg  # replace main module
	sed -i 's#$(_expr_assig)$(_expr_sub)#\1$(_prj_main)#g' $(_prj_files)             # replace current main in copied files
	sed -i 's#$(PRJ)#$(NEW_PRJ)#g'                         $(_prj_files)             # replace current project in copied files
	touch $(_prj_package)/__init__.py       # create python package
	touch $(_prj_package)/__main__.py       # make package runnable
	test -e $(_prj_test) || echo '$(_prj_test_def)' > $(_prj_test)  # create a test file
	$(_diff) . $(_prj_path) || true         # compare the copied files to the source files
	#-------------------------------------------
	# Cloned $(PRJ) to $(_prj_path)!
	# If all went well you can now build it
	#-------------------------------------------
	@echo cd $(_prj_path)
	@echo make
	@echo make dist
	# -------------------------------------------

clone-project: check-clone merge-project
