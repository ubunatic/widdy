.PHONY: test clean install publish dist test-publish

all: clean test

test:
	python3 -m flake8
	pytest-3 -s widdy

clean:
	pyclean .
	rm -rf .cache dist build ohlcwid.egg-info

install:
	pip3 install --user -e .

dist: clean
	python3 setup.py bdist_wheel
	gpg --detach-sign -a dist/*.whl
	ls dist

test-publish: dist test
	twine upload --repository testpypi dist/*

publish: dist test
	twine upload --repository pypi dist/*

docker-test:
	docker run -it python bash -it -c 'pip install widdy; widdy all'
