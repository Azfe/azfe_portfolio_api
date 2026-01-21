# Portfolio - API

API REST desarrollada con FastAPI para gestionar dinámicamente los datos de mi CV y portafolio profesional. Este backend alimenta tanto mi sitio web personal como la versión descargable de mi currículum.

## 🌐 Ecosistema del Proyecto

Este repositorio forma parte de un ecosistema de 3 aplicaciones:

- [azfe_portfolio_api](https://github.com/Azfe/azfe_portfolio_api) - API REST (FastAPI + MongoDB) ← 📍
- [azfe_portfolio_astro](https://github.com/Azfe/azfe_portfolio_astro) -  Sitio web principal (Astro + Tailwind CSS)
- [azfe_portfolio_cv](https://github.com/Azfe/azfe_portfolio_cv) - CV descargable (HTML + SCSS + JavaScript)

## 💻 Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

## 🚀 Inicio Rápido con Docker (Recomendado)

### Requisitos Previos

- Docker Desktop instalado
- Make (opcional, facilita comandos)

### Levantar el entorno

```bash
# 1. Clonar el repositorio
git clone 
cd azfe_portfolio_backend

# 2. Copiar variables de entorno
cp .env.example .env.development

# 3. Levantar servicios con Make
make build
make up

# O sin Make:
cd deployments
docker compose build
docker compose up -d
```

### Verificar que funciona

- **API**: [http://localhost:8000](http://localhost:8000)
- **Documentación**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### Comandos útiles

```bash
# Ver logs en tiempo real
make logs

# Ejecutar tests
make test

# Abrir shell en el contenedor
make shell

# Reiniciar servicios
make restart

# Detener servicios
make down

# Limpiar todo
make clean
```

## 📦 Instalación local (Sin Docker)

Si prefieres no usar Docker:

### 1. Clonar el repositorio

```bash
git clone git@github.com:Azfe/mi_portfolio_api.git
cd mi_portfolio_api
```

### 2. Crear y activar el entorno virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

MacOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 🔄 Actualizar dependencias (opcional)

```bash
# Reinstalar todas las dependencias
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# Actualizar un paquete específico
pip install --upgrade nombre-del-paquete
```

### 4. Configurar variables de entorno

Crea un archivo `config.env` dentro de `app/core/`:

```bash
MONGO_URI=your_mongodb_connection_uri
JWT_SECRET_KEY=your_secret_key
```

> **Nota:** *También puedes exportar estas variables directamente en tu sistema operativo.*

### 5. Configurar la base de datos

Asegúrate de tener MongoDB instalado y crea una base de datos llamada jimcostdev_api con las siguientes colecciones:

- `contact`
- `education`
- `perfil`
- `projects`
- `social_networks`
- `work_experience`
- `users`

### 6. Ejecutar el servidor

```bash
cd app
fastapi dev main.py
```

## 🧪 Testing

```bash
# Con Docker
make test

# Sin Docker
pytest

# Con coverage
pytest --cov=app --cov-report=html

## 📖 Documentación de la API

Después de iniciar la aplicación, la documentación está disponible en:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
- Comprobación de estado: `http://localhost:8000/ping`

> **Nota:** *También puedes usar herramientas como Postman o Insomnia para probar los endpoints.*

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar algo, abre un pull request o crea un issue.

1. Hacer fork del proyecto
2. Crear una rama de características (`git checkout -b feature/amazing-feature`)
3. Confirmar los cambios (`git commit -m 'Add amazing feature`)
4. Push hacia la rama (`git push origin feature/amazing-feature`)
5. Abrir una solicitud de extracción

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🧑‍💻 Autor

Azfe - [alexzapata1984@gmail.com](mailto:alexzapata1984@gmail.com)
