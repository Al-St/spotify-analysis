PYTHON := .venv/bin/python
UV := uv

.PHONY: install run test lint format notebook clean

install: ## создать venv и установить пакет с dev-зависимостями
	$(UV) venv .venv --python 3.12
	$(UV) pip install --python .venv -e ".[dev]"

run: ## пересобрать таблицы и диаграммы в reports/
	$(PYTHON) -m spotify_analysis

test: ## прогнать тесты
	$(PYTHON) -m pytest

lint: ## проверить код линтером
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

format: ## автоматически отформатировать код
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

notebook: ## открыть аналитический ноутбук
	.venv/bin/jupyter lab notebooks/spotify_2024_analysis.ipynb

clean: ## удалить кэши и сборочные артефакты
	rm -rf .pytest_cache .ruff_cache dist build *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
