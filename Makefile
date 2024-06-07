# Makefile for https://github.com/marhar/llmuri

# Variables
PACKAGE_NAME=llmuri
VERSION=0.1.0
PYTHON=python
TWINE=twine

# Default target
all: build

# Clean up build directories
clean:
	rm -rf build dist *.egg-info
	rm -rf examples/__pycache__
	rm -rf llmuri/__pycache__
	rm -rf tests/__pycache__

# Build the package
build: clean
	$(PYTHON) setup.py sdist bdist_wheel

# Run tests
test:
	$(PYTHON) -m unittest discover -s tests

upload-testpypi: build
	$(TWINE) upload --repository-url https://packaging.python.org/en/latest/tutorials/packaging-projects/ dist/*

upload-pypi: build
	$(TWINE) upload dist/*

install-testpypi:
	pip install --index-url https://test.pypi.org/simple/ $(PACKAGE_NAME)==$(VERSION)

install-pypi:
	pip install --index-url https://pypi.org/simple/ $(PACKAGE_NAME)==$(VERSION)

release-testpypi: test build upload-testpypi install-testpypi

help:
	@echo "Makefile for llmuri package"
	@echo ""
	@echo "Usage:"
	@echo "  make clean               Clean up build directories"
	@echo "  make build               Build the package"
	@echo "  make test                Run tests"
	@echo "  make upload-testpypi     Upload package to TestPyPI"
	@echo "  make install-testpypi    Install package from TestPyPI"
	@echo "  make release-testpypi    Run tests, build, upload to TestPyPI, and install"
	@echo "  make help                Show this help message"

.PHONY: all clean build test upload-testpypi install-testpypi release-testpypi help
