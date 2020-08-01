.PHONY:	all
all:

.PHONY:	init
init:
	pip install -r requirements.txt

.PHONY:	check
check:

.PHONY:	docs
docs:

.PHONY:	dist
dist:	check
	python setup.py sdist bdist_wheel
	twine upload dist/*
