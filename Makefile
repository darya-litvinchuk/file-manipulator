# Place your local stuff in Makefile.local
-include .env
-include Makefile.local

PROJECT_DIRECTORY='src/'


.PHONY: format
format:
	@#@ Run formatting using black and isort
	black ${PROJECT_DIRECTORY} && isort ${PROJECT_DIRECTORY}


.PHONY: format-check
format-check:
	@#@ Run formatting using black and isort
	black ${PROJECT_DIRECTORY} --check && isort ${PROJECT_DIRECTORY} --check


.PHONY: flake8
flake8:
	@#@ Run flake8
	flake8 ${PROJECT_DIRECTORY}


.PHONY: mypy-check
mypy-check:
	@#@ Run typechecking using mypy
	mypy ${PROJECT_DIRECTORY}


.PHONY: lint
lint:
	@#@ Run all linters linter
	make format-check
	make flake8
	make mypy-check


.PHONY: mypy-check
licenses-check:
	@#@ Run typechecking using mypy
	pip-licenses --summary
	pip-licenses --from=classifier --order=license


.PHONY: tests
tests:
	@#@ Run tests
	pytest --no-cov || true


.PHONY: tests-coverage
tests-coverage:
	@#@ Test coverage report
	pytest --cov-report term-missing:skip-covered || true


.PHONY: mutmut-check
mutmut-check:
	@#@ Test application tests
	mutmut run; mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut-report.xml


.PHONY: radon-check
radon-check:
	@#@ Check project source code metrics
	radon mi ${PROJECT_DIRECTORY}
	radon cc ${PROJECT_DIRECTORY} -a


.PHONY: clean-cache
clean-cache:
	@#@ Clean junk files
	find . -name \*.pyc -delete
	find . -name __pycache__ -exec rm -rf {} \;
	rm -rf *.egg-info
