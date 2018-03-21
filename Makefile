.PHONY: test clean install publish

all: clean test

test:
	python3 -m flake8
	pytest-3 -s widdy

clean:
	pyclean .
	rm -rf .cache dist build ohlcwid.egg-info

install:
	python3 setup.py bdist_wheel
	pip3 install --user -e .

publish:
	gpg --detach-sign -a dist/widdy-0.2.0-py3-none-any.whl
	# twine upload
