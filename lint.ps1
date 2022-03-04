$ErrorActionPreference = "Stop"

& poetry run black .
& poetry run isort .
& poetry run flake8 .
& poetry run pydocstyle
& poetry run pytest
