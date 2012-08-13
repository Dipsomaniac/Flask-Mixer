.PHONY: clean
clean:
	sudo rm -rf build dist
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

.PHONY: upload
upload:
	python setup.py sdist upload || echo 'Upload already'

.PHONY: register
register:
	python setup.py register

.PHONY: test
test:
	python setup.py test
