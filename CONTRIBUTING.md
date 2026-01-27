# 🤝 Contribuciones

## 📋 Requisitos previos

Antes de contribuir al proyecto, asegúrate de tener instalado y configurado el siguiente entorno. Esto garantiza que todos los colaboradores trabajen bajo las mismas condiciones y evita errores desde el primer momento.

### 🐍 Python

El backend utiliza:

**Python 3.13.7**

Asegúrate de tener esta versión instalada. Puedes verificarla con:

```bash
python --version
```

### 🐳 Docker (opcional pero recomendable)

Docker no es obligatorio para contribuir, pero sí es recomendable para:

- Ejecutar MongoDB sin instalarlo localmente
- Probar el backend en un entorno aislado
- Reproducir el entorno de producción

Si deseas usarlo:

- Instala Docker Desktop o Docker Engine
- Verifica con:

```bash
docker --version
```

### 🧰 Editor recomendado: Visual Studio Code

Se recomienda usar VSCode junto con las siguientes extensiones:

- Python
- Pylance
- Python Indent
- Prettier
- Black Formatter
- GitLens
- Container Tools

Estas extensiones ayudan a mantener un estilo de código consistente, mejorar la productividad y facilitar el trabajo con Docker y Git.

---

## 🗼 Estructura del proyecto

Este backend sigue una arquitectura basada en **Clean Architecture**, separando claramente dominio, casos de uso, infraestructura y API.  
Cada capa tiene responsabilidades estrictas para mantener el sistema modular, testeable y fácil de mantener.

---

### 🧱 Capas principales

#### 🔹 1. `domain/` — Dominio (Reglas de negocio puras)

Contiene la lógica central del sistema, completamente independiente de frameworks o infraestructura.

Incluye:

- **Entities** → Modelos de negocio (Python puro)
- **Value Objects** → Objetos inmutables con validación interna
- **Domain Exceptions** → Errores propios del dominio

**Reglas:**

- ❌ No usar Pydantic  
- ❌ No acceder a la base de datos  
- ❌ No importar nada de `infrastructure/` ni `api/`  
- ✔️ Solo lógica de negocio pura  

---

#### 🔹 2. `application/` — Casos de uso

Orquesta la lógica del dominio y coordina repositorios, mappers y DTOs.

Incluye:

- **Use Cases** (uno por acción del sistema)
- **DTOs** (para transportar datos entre capas)

**Reglas:**

- ❌ No acceder directamente a MongoDB  
- ❌ No usar modelos Pydantic  
- ✔️ Debe depender solo de `domain/` y `shared/`  
- ✔️ Debe usar interfaces (`IRepository`, `IMapper`)  

---

#### 🔹 3. `infrastructure/` — Infraestructura

Implementa detalles técnicos del sistema.

Incluye:

- **Database** (MongoDB client, colecciones)
- **Repositories** (implementaciones concretas)
- **Mappers** (Domain ↔ Persistence)

**Reglas:**

- ❌ No incluir lógica de negocio  
- ❌ No llamar casos de uso  
- ✔️ Implementa interfaces definidas en `shared/interfaces`  
- ✔️ Puede usar Pydantic solo para persistencia si es necesario  

---

#### 🔹 4. `api/` — Presentación (FastAPI)

Expone los endpoints HTTP y gestiona la comunicación con el exterior.

Incluye:

- **Routers** (endpoints)
- **Schemas** (Pydantic)
- **Dependencies**
- **Middlewares**
- **Exception Handlers**

**Reglas:**

- ❌ No acceder directamente a la base de datos  
- ❌ No instanciar repositorios concretos dentro de los routers  
- ❌ No incluir lógica de negocio  
- ✔️ Debe llamar a casos de uso  
- ✔️ Debe validar entrada/salida con Pydantic  

---

#### 🔹 5. `shared/` — Código común

Incluye:

- **Interfaces** (repositorios, mappers, casos de uso)
- **Excepciones base**
- **Tipos comunes**
- **Utilidades**

**Reglas:**

- ✔️ Puede ser usado por todas las capas  
- ❌ No debe depender de infraestructura ni API  

---

#### 🔹 6. `config/` — Configuración

Incluye:

- Variables de entorno
- Settings de la aplicación

**Reglas:**

- ✔️ Puede ser usado por API e infraestructura  
- ❌ No debe contener lógica de negocio  

---

#### 🔹 7. `tests/` — Pruebas

Organizado por capas:

- `unit/` → dominio y aplicación  
- `integration/` → infraestructura y API  
- `e2e/` → flujo completo  

---

### 🚫 Qué NO debe hacerse (reglas estrictas)

Para mantener la arquitectura limpia:

#### ❌ No acceder a la base de datos desde

- Routers (`api/`)
- Casos de uso (`application/`)
- Entidades o value objects (`domain/`)

#### ❌ No usar Pydantic en

- Dominio  
- Casos de uso  

#### ❌ No mezclar responsabilidades

- Nada de lógica de negocio en routers  
- Nada de lógica de negocio en repositorios  
- Nada de lógica de infraestructura en casos de uso  

#### ❌ No importar hacia “adentro”

Las dependencias deben ir siempre:

```text
domain → application → infrastructure → api
```

Nunca al revés.

---

### ✔️ Resumen visual

```text
domain/          → Reglas de negocio puras
application/     → Casos de uso
infrastructure/  → Repositorios, DB, mappers
api/             → Endpoints, schemas, middlewares
shared/          → Interfaces, excepciones, utilidades
config/          → Configuración
tests/           → Pruebas
```

---

Esta sección garantiza que cualquier colaborador entienda cómo está organizado el backend y qué reglas debe respetar para no romper la arquitectura.

---

## 🚀 Flujo de trabajo con Git

Este proyecto sigue un flujo de trabajo basado en ramas feature, commits semánticos y **Pull Requests revisados**.

El objetivo es mantener un historial limpio, predecible y fácil de mantener.

### 1️⃣ Hacer fork del repositorio

1. En GitHub, ve al repositorio principal.

2. Haz clic en Fork (arriba a la derecha).

3. Crea tu copia del repositorio en tu cuenta.

Tu fork será algo como:

```text
https://github.com/<tu-usuario>/<nombre-del-proyecto>
```

### 2️⃣ Clonar tu fork

Clona tu copia del repositorio:

```bash
git clone https://github.com/<tu-usuario>/<nombre-del-proyecto>.git
cd <nombre-del-proyecto>
```

### 3️⃣ Configurar el remoto del repositorio original (upstream)

Esto permite sincronizar tu fork con el proyecto principal:

```bash
git remote add upstream https://github.com/<owner>/<nombre-del-proyecto>.git
```

Verifica:

```bash
git remote -v
```

Debes ver:

- `origin` → tu fork
- `upstream` → repo original

### 4️⃣ Crear ramas nuevas

Nunca trabajes directamente en `main`.
Crea una rama nueva basada en el `main` del repositorio original.

Primero sincroniza:

```bash
git checkout main
git pull upstream main
git push origin main
```

Luego crea tu rama:

```bash
git checkout -b feature/<id>-<descripcion>
```

Ejemplos:

```text
feature/#1-create-contributing-doc
fix/#102-invalid-date-validation
docs/#77-update-readme
```

### 5️⃣ Convención de nombres de ramas

Formato:

```text
<tipo>/<id>-<descripcion>
```

Tipos permitidos:

- `feature/` → nuevas funcionalidades
- `fix/` → corrección de bugs
- `refactor/` → mejoras internas
- `docs/` → documentación
- `test/` → pruebas
- `chore/` → tareas varias

Reglas:

- `<id>` = número de issue
- `<descripcion>` = minúsculas, con guiones, corta y clara

### 6️⃣ Sincronizar tu rama con main (del repo original)

Si el proyecto avanza mientras trabajas, actualiza tu rama:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

Luego actualiza tu rama:

```bash
git checkout feature/<id>-<descripcion>
git merge main
```

### 7️⃣ Hacer commits (Conventional Commits)

Usamos Conventional Commits.

Formato:

```text
<tipo>(<scope>): <mensaje>
```

Tipos comunes:

- `feat`: nueva funcionalidad
- `fix`: corrección de bug
- `refactor`: mejora interna
- `docs`: documentación
- `test`: pruebas
- `chore`: tareas varias

Ejemplos:

```text
feat(profile): add profile creation use case
fix(api): correct validation error in POST /profile
docs(contributing): add git workflow section
```

### 8️⃣ Hacer push a tu fork

```bash
git push -u origin feature/<id>-<descripcion>
```

Si ya existe:

```bash
git push
```

### 9️⃣ Abrir un Pull Request (PR)

1. Ve a tu fork en GitHub.
2. Haz clic en Compare & Pull Request.
3. Asegúrate de que el PR va hacia:

```text
base: main (del repo original)
compare: feature/<id>-<descripcion> (de tu fork)
```

4. Completa la plantilla del PR.
5. Incluye la referencia a la issue:

```text
Closes #51
```

6. Revisa el checklist:

- [ ] Código formateado
- [ ] Linter sin errores
- [ ] Tests pasando
- [ ] Documentación actualizada
- [ ] Issue vinculada

7. Envía el PR y espera revisión.
