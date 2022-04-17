test:
	PYTHONPATH=src/ pytest

fmt:
	black . && isort . && flake8 .
