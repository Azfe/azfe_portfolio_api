# Makefile - Comandos simplificados para desarrollo

.PHONY: help build up down restart logs shell test clean seed test-cov test-unit test-integration test-mark coverage-report test-clean

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
	@echo "  make test-cov  - Tests con coverage report HTML"
	@echo "  make test-unit - Tests solo unitarios"
	@echo "  make test-integration - Tests solo de integración"
	@echo "  make test-mark - Tests con marcador específico (ej: make test-mark MARK=slow)"
	@echo "  make coverage-report - Ver reporte de coverage"
	@echo "  make seed      - Inicializar base de datos con datos de prueba"
	@echo "  make clean     - Limpiar contenedores y volúmenes"
	@echo "  make test-clean - Limpiar archivos de test"

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

# Inicializar base de datos con datos de prueba
seed:
	cd deployments && docker compose exec backend python scripts/seed_data.py

# Tests
# Ejecutar tests dentro del contenedor (comando por defecto)
test:
	cd deployments && docker compose exec backend pytest

# Tests con coverage
test-cov:
	cd deployments && docker compose exec backend pytest --cov=app --cov-report=html

# Tests solo unitarios
test-unit:
	cd deployments && docker compose exec backend pytest tests/unit -v

# Tests solo de integración
test-integration:
	cd deployments && docker compose exec backend pytest tests/integration -v

# Tests con marcador específico
test-mark:
ifndef MARK
	@echo "❌ Error: Debes especificar un marcador. Uso: make test-mark MARK=nombre_marcador"
	@exit 1
endif
	cd deployments && docker compose exec backend pytest -m $(MARK)

# Ver reporte de coverage
coverage-report:
	@echo "Abriendo reporte de coverage..."
	@if command -v open > /dev/null 2>&1; then \
		open htmlcov/index.html; \
	elif command -v xdg-open > /dev/null 2>&1; then \
		xdg-open htmlcov/index.html; \
	else \
		echo "Reporte disponible en: htmlcov/index.html"; \
	fi

# Limpiar contenedores, imágenes y volúmenes
clean:
	cd deployments && docker compose down -v
	@echo "✅ Contenedores y volúmenes eliminados"

# Limpiar archivos de test
test-clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Archivos de test limpiados"