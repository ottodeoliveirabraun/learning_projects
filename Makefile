deps:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pip install pytest pytest-md pytest-emoji pytest-cov
	python -m pytest tests/ --cov-report term --cov-report xml:coverage.xml --cov=.
