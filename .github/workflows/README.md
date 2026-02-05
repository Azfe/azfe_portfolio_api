# GitHub Actions Workflows

Este directorio contiene los workflows de CI/CD para el proyecto Portfolio Backend.

## 📋 Workflows Disponibles

### 1. **lint.yml** - Code Quality & Linting

Ejecuta verificaciones de calidad de código en cada push y pull request.

**Verifica:**
- ✅ **Black**: Formateo de código
- ✅ **Isort**: Ordenamiento de imports
- ✅ **Ruff**: Linting general
- ✅ **MyPy**: Type checking
- ✅ **Bandit**: Análisis de seguridad
- ✅ **Safety**: Vulnerabilidades en dependencias

**Se ejecuta en:**
- Python 3.12 y 3.13
- Branches: `main`, `develop`, `feature/**`

### 2. **tests.yml** - Tests

Ejecuta todos los tests del proyecto con cobertura.

**Incluye:**
- 🧪 Tests unitarios
- 🔗 Tests de integración
- 🌐 Tests end-to-end
- 📊 Reporte de cobertura (Codecov)
- 🗄️ MongoDB 8.0 service

**Se ejecuta en:**
- Python 3.12 y 3.13
- Branches: `main`, `develop`, `feature/**`

## 🔐 Configuración de Secretos

Para que los workflows funcionen correctamente, necesitas configurar los siguientes secretos en GitHub:

### Pasos para configurar secretos:

1. Ve a tu repositorio en GitHub
2. Click en `Settings` > `Secrets and variables` > `Actions`
3. Click en `New repository secret`
4. Agrega los siguientes secretos:

### Secretos Requeridos:

#### **CODECOV_TOKEN** (Opcional pero recomendado)
Para subir reportes de cobertura a Codecov.

```
1. Ve a https://codecov.io/
2. Conecta tu repositorio de GitHub
3. Copia el token de Codecov
4. Agrégalo como secreto en GitHub con el nombre: CODECOV_TOKEN
```

#### **MONGODB_URL** (Opcional)
URL de conexión a MongoDB para tests. Si no se configura, usa `mongodb://localhost:27017` por defecto.

```
Nombre: MONGODB_URL
Valor: mongodb://localhost:27017
```

#### **SECRET_KEY** (Futuro)
Clave secreta para la aplicación. Si no se configura, usa un valor por defecto para testing.

```
Nombre: SECRET_KEY
Valor: tu-clave-secreta-aqui
```

## 📊 Badges para README

Puedes agregar estos badges a tu README.md principal:

```markdown
![Code Quality](https://github.com/USUARIO/REPO/workflows/Code%20Quality%20&%20Linting/badge.svg)
![Tests](https://github.com/USUARIO/REPO/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/USUARIO/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USUARIO/REPO)
```

Reemplaza `USUARIO` y `REPO` con tu información.

## 🚀 Ejecución Manual

Puedes ejecutar los workflows manualmente desde la pestaña "Actions" en GitHub:

1. Ve a la pestaña `Actions`
2. Selecciona el workflow que quieres ejecutar
3. Click en `Run workflow`
4. Selecciona la branch
5. Click en `Run workflow`

## 🔧 Configuración Local

Para ejecutar las mismas validaciones localmente:

### Code Quality:

```bash
# Formateo
black app/ tests/
isort app/ tests/

# Linting
ruff check app/ tests/

# Type checking
mypy app/

# Security
bandit -r app/
safety check
```

### Tests:

```bash
# Todos los tests
pytest tests/ -v

# Solo unitarios
pytest tests/unit/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html

# En paralelo
pytest tests/ -n auto
```

## 📁 Estructura de Artifacts

Los workflows generan artifacts que puedes descargar:

### Lint Workflow:
- `bandit-report-py3.12.json`
- `bandit-report-py3.13.json`

### Tests Workflow:
- `test-results-unit-py3.12/`
- `test-results-integration-py3.12/`
- `test-results-e2e-py3.12/`
- (Similar para Python 3.13)

Cada artifact incluye:
- Archivo JUnit XML con resultados
- Reporte HTML de cobertura

## 🐛 Troubleshooting

### Error: "MongoDB not ready"

Si los tests fallan porque MongoDB no está listo:
- El workflow ya incluye un paso `Wait for MongoDB`
- Aumenta el tiempo de espera si es necesario

### Error: "Module not found"

Si falta alguna dependencia:
1. Verifica que esté en `requirements-dev.txt`
2. Haz commit y push de los cambios
3. El workflow instalará la nueva dependencia

### Error: "Coverage upload failed"

Si Codecov falla:
- Verifica que el token `CODECOV_TOKEN` esté configurado
- El workflow está configurado con `fail_ci_if_error: false`, así que no bloqueará el CI

## 📖 Documentación Adicional

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Codecov Documentation](https://docs.codecov.com/)
- [pytest Documentation](https://docs.pytest.org/)
