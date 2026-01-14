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

## 📦 Instalación

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

🔄 Actualizar dependencias (opcional):

```bash
# Reinstalar todas las dependencias
pip uninstall -y -r requirements.txt
pip install -r requirements.txt


# Actualizar un paquete específico

```bash
pip install --upgrade nombre-del-paquete
```

### 4. Configurar variables de entorno

Crea un archivo `config.env` dentro de `app/core/`:

```bash
MONGO_URI=your_mongodb_connection_uri
JWT_SECRET_KEY=your_secret_key
```

*También puedes exportar estas variables directamente en tu sistema operativo.*

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

La API estará disponible en `http://localhost:8000`

## 📖 Documentación

Accede a la documentación interactiva de la API:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

*También puedes usar herramientas como Postman o Insomnia para probar los endpoints.*

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar algo, abre un pull request o crea un issue.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 📬 Contacto

Para contactarme, escribe a [alexzapata1984@gmail.com](mailto:alexzapata1984@gmail.com)
