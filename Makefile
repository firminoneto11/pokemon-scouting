cov := coverage run -m pytest
cov_port := 5500
url := http://localhost:$(cov_port)

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

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -c "import webbrowser; webbrowser.open_new_tab('$(url)')"
	python -m http.server -d .coverage/html-report $(cov_port)

test:
	docker build -t pokemon-scouting-testing --file docker/testing/Dockerfile .
	docker run --rm pokemon-scouting-testing
	docker rmi pokemon-scouting-testing
