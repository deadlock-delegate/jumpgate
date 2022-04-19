test:
	PYTHONPATH=src/ pytest

fmt:
	black . && isort . && flake8 .


start:
	PYTHONPATH=src/ python src/jumpgate/main.py
