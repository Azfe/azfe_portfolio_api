# Tests del Backend

## Estructura

```text-plain
tests/
├── unit/               # Tests unitarios
├── integration/        # Tests de integración
├── e2e/               # Tests end-to-end
├── fixtures/          # Datos de prueba
└── conftest.py        # Configuración global
```

## Ejecutar Tests

### Con Make (Docker)

```bash
# Todos los tests
make test

# Solo unitarios
make test-unit

# Solo integración
make test-integration

# Con coverage
make test-cov

# Ver reporte de coverage
make coverage-report
```

### Sin Docker

```bash
# Todos los tests
pytest

# Con marcador específico
pytest -m unit

# Solo un archivo
pytest tests/unit/test_config.py

# Con coverage
pytest --cov=app
```

## Escribir Tests

### Test Unitario

```python
def test_something():
    result = function_to_test()
    assert result == expected_value
```

### Test de Integración

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_endpoint(client):
    response = await client.get("/api/v1/endpoint")
    assert response.status_code == 200
```

## Marcadores

- `@pytest.mark.unit`: Tests unitarios
- `@pytest.mark.integration`: Tests de integración
- `@pytest.mark.e2e`: Tests end-to-end
- `@pytest.mark.slow`: Tests lentos

## Fixtures Disponibles

- `client`: Cliente HTTP para testear endpoints
- `test_db`: Base de datos de test limpia
- `sample_profile_data`: Datos de ejemplo para Profile
- `sample_skill_data`: Datos de ejemplo para Skill
