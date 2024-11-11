# Variáveis
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

# Alvo padrão
.DEFAULT_GOAL := help

# Checa se Python está instalado
.PHONY: check-python
check-python:
	@command -v python3 >/dev/null 2>&1 || { \
		echo >&2 "Python não encontrado. Instalando Python..."; \
		sudo apt update && sudo apt install -y python3 python3-venv; \
	}

# Alvos
.PHONY: help
help:  ## Mostra a lista de comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: check-python ## Cria um ambiente virtual em .venv
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

.PHONY: install
install: venv ## Instala as dependências do projeto
	$(PIP) install -r requirements.txt

.PHONY: test
test: ## Executa testes
	$(PYTHON) -m unittest discover -s tests

.PHONY: lint
lint: ## Verifica o estilo do código com flake8
	$(PYTHON) -m flake8 src/

.PHONY: format
format: ## Formata o código com black
	$(PYTHON) -m black src/

.PHONY: clean
clean: ## Remove arquivos temporários e o ambiente virtual
	rm -rf $(VENV) __pycache__ */__pycache__ .mypy_cache .pytest_cache
