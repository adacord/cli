.PHONY: help
help:
	@echo "install-ci - install development dependencies for continuous integration"

.PHONY: install-base
# Install base setup tools
install-base:
	python -m pip install -U pip setuptools poetry wheel

.PHONY: install
# Install the dependencies needed for a production installation
install:: install-base
	poetry install --no-dev

.PHONY: install-ci
# Install the tools necessary for CI
install-ci:: install-base

install-ci::
	poetry install
