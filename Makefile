test:
	PYTHONPATH=src/ pytest

fmt:
	black . && isort . && flake8 .


start:
	PYTHONPATH=src/ python src/portal/main.py
