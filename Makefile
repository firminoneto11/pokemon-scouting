env:
	rm -rf .venv/
	uv venv -p 3.13

deps:
	uv sync --no-install-project --frozen

dev:
	python3 manage.py runserver

pc:
	pre-commit run --config .pre-commit-config.yaml --all-files

up:
	docker compose -f docker/staging/docker-compose.yaml up

down:
	docker compose -f docker/staging/docker-compose.yaml down --volumes --rmi all
