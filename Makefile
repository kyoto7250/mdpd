style:
	poetry run black mdpd/ tests/
	poetry run isort mdpd/ tests/
	poetry run ruff  mdpd/ tests/

test:
	poetry run  pytest
