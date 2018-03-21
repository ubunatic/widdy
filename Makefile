.PHONY: test
test:
	pytest-3 -s

clean:
	pyclean .
	rm -rf .cache
