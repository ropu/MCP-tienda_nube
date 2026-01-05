.PHONY: help build start stop restart logs status update clean health info test

# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3
PIP = pip3

help:
	@echo "Tienda Nube API MCP Server - Comandos disponibles"
	@echo ""
	@echo "Desarrollo:"
	@echo "  make install       Instalar dependencias"
	@echo "  make test          Ejecutar pruebas"
	@echo "  make lint          Ejecutar linter"
	@echo "  make format        Formatear código"
	@echo ""
	@echo "Docker:"
	@echo "  make build         Construir imagen Docker"
	@echo "  make start         Iniciar servicios"
	@echo "  make stop          Detener servicios"
	@echo "  make restart       Reiniciar servicios"
	@echo "  make logs          Ver logs"
	@echo "  make status        Ver estado"
	@echo "  make clean         Limpiar contenedores"
	@echo ""
	@echo "Monitoreo:"
	@echo "  make health        Verificar salud"
	@echo "  make info          Obtener información"
	@echo "  make update        Actualizar y reiniciar"
	@echo ""

# ============================================================================
# Desarrollo
# ============================================================================

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) test_server.py

lint:
	flake8 server_simple.py app.py --max-line-length=100
	black --check server_simple.py app.py

format:
	black server_simple.py app.py
	isort server_simple.py app.py

# ============================================================================
# Docker
# ============================================================================

build:
	$(DOCKER_COMPOSE) build --no-cache

start:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

restart: stop start

logs:
	$(DOCKER_COMPOSE) logs -f

logs-mcp:
	$(DOCKER_COMPOSE) logs -f mcp-server

logs-nginx:
	$(DOCKER_COMPOSE) logs -f nginx

status:
	$(DOCKER_COMPOSE) ps

clean:
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) down --rmi all

# ============================================================================
# Monitoreo
# ============================================================================

health:
	@curl -s http://localhost:8000/health | $(PYTHON) -m json.tool

info:
	@curl -s http://localhost:8000/info | $(PYTHON) -m json.tool

update: stop build start

# ============================================================================
# Utilidades
# ============================================================================

shell-mcp:
	$(DOCKER_COMPOSE) exec mcp-server /bin/bash

shell-nginx:
	$(DOCKER_COMPOSE) exec nginx /bin/sh

backup:
	@mkdir -p backups
	@docker exec tiendanube-mcp-server cat /app/api_database.json > backups/api_database_$(shell date +%Y%m%d_%H%M%S).json
	@echo "Backup creado en backups/"

restore:
	@read -p "Ingresa el archivo de backup: " backup_file; \
	docker cp $$backup_file tiendanube-mcp-server:/app/api_database.json; \
	$(DOCKER_COMPOSE) restart mcp-server

# ============================================================================
# Desarrollo local
# ============================================================================

dev:
	$(PYTHON) app.py

dev-test:
	$(PYTHON) -m pytest test_server.py -v

# ============================================================================
# Limpieza
# ============================================================================

clean-logs:
	rm -rf logs/*
	mkdir -p logs/nginx

clean-ssl:
	rm -rf ssl/*

clean-all: clean clean-logs clean-ssl
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete

.DEFAULT_GOAL := help
