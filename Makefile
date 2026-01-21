# Makefile - Comandos simplificados para desarrollo

.PHONY: help build up down restart logs shell test clean

# Mostrar ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make build     - Construir imágenes Docker"
	@echo "  make up        - Levantar servicios"
	@echo "  make down      - Detener servicios"
	@echo "  make restart   - Reiniciar servicios"
	@echo "  make logs      - Ver logs en tiempo real"
	@echo "  make shell     - Abrir shell en el contenedor backend"
	@echo "  make test      - Ejecutar tests"
	@echo "  make clean     - Limpiar contenedores y volúmenes"

# Construir imágenes
build:
	cd deployments && docker compose build

# Levantar servicios
up:
	cd deployments && docker compose up -d
	@echo "✅ Servicios levantados"
	@echo "📍 API: http://localhost:8000"
	@echo "📍 Docs: http://localhost:8000/docs"
	@echo "📍 MongoDB: localhost:27017"

# Detener servicios
down:
	cd deployments && docker compose down

# Reiniciar servicios
restart: down up

# Ver logs en tiempo real
logs:
	cd deployments && docker compose logs -f

# Logs solo del backend
logs-backend:
	cd deployments && docker compose logs -f backend

# Logs solo de MongoDB
logs-mongodb:
	cd deployments && docker compose logs -f mongodb

# Abrir shell en el contenedor backend
shell:
	cd deployments && docker compose exec backend bash

# Ejecutar tests dentro del contenedor
test:
	cd deployments && docker compose exec backend pytest

# Limpiar contenedores, imágenes y volúmenes
clean:
	cd deployments && docker compose down -v
	@echo "✅ Contenedores y volúmenes eliminados"

# Inicializar base de datos con datos de prueba
seed:
	cd deployments && docker compose exec backend python scripts/seed_data.py