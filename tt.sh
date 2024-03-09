poetry run python -m coverage run --source=src -m unittest
poetry run python -m coverage report -m --fail-under=100
poetry run coverage xml

poetry run mypy .
poetry run ruff check .
poetry run ruff format
