# PROJECT_CONTEXT.md  

**Portfolio Backend & Frontend – Contexto General del Proyecto**

Este documento sirve como **paquete de contexto** para cualquier desarrollador, colaborador o herramienta que necesite entender el proyecto rápidamente.  
Define el propósito, alcance, arquitectura, reglas internas, estado actual, roadmap y estándares del proyecto.

---

## 1. Propósito del proyecto

El objetivo principal es construir un **portfolio profesional moderno, escalable y administrable**, que permita:

- Presentar el perfil profesional de forma clara y estructurada.  
- Mostrar proyectos, habilidades, certificaciones y experiencia.  
- Facilitar el contacto con empleadores o colaboradores.  
- Gestionar todo el contenido mediante un backend robusto, validado y mantenible.  
- Demostrar estándares profesionales de ingeniería: arquitectura, calidad, claridad y buenas prácticas.

**Mensaje que transmite el proyecto:**  
> “Sé construir algo simple, pero bien diseñado. Sé separar capas, pensar en datos, APIs, despliegue y cuidar los detalles.”

---

## 2. Descripción general del backend

Backend construido con **FastAPI**, **MongoDB** y **Clean Architecture**, que expone una API REST versionada para gestionar todos los recursos del portfolio:

- Perfil  
- Experiencia laboral  
- Educación  
- Skills  
- Herramientas  
- Proyectos  
- Certificaciones  
- Idiomas  
- Redes sociales  
- Información de contacto  
- Mensajes de contacto  
- CV completo  
- Generación de PDF del CV  

El backend aplica reglas de negocio, validaciones, mapeos, casos de uso y persistencia desacoplada.

---

## 3. Descripción general del frontend

El frontend está desarrollado con **Astro** y se encarga de:

- Renderizar el portfolio completo.  
- Mostrar todas las secciones del CV.  
- Proveer la interfaz visual del CV (HTML + CSS).  
- Consumir la API REST del backend.  
- Enviar mensajes de contacto.  
- Solicitar la descarga del CV en PDF.  

Comunicación con el backend:

- Protocolo: **HTTPS**  
- Formato: **JSON** (datos) y **application/pdf** (CV)  
- Método: `fetch()` o utilidades de Astro  
- CORS habilitado desde el backend  

---

## 4. Arquitectura del backend (resumen)

El backend sigue **Clean Architecture** con capas bien definidas:

- **API**: routers, schemas, middlewares, exception handlers  
- **Application**: casos de uso, DTOs  
- **Domain**: entidades, value objects, reglas de negocio  
- **Infrastructure**: repositorios, mappers, base de datos, PDF service  
- **Shared**: interfaces, excepciones, tipos comunes  

Regla de dependencia:  
> Las dependencias siempre apuntan hacia adentro.  
> Domain nunca conoce Application, API ni Infrastructure.

---

## 5. Flujos clave del sistema

Los flujos principales documentados en ARCHITECTURE.md son:

1. Obtener perfil completo  
2. Actualizar perfil  
3. Añadir experiencia laboral  
4. Obtener CV completo  
5. Generar PDF del CV  
6. Enviar mensaje de contacto  

Estos flujos describen cómo viaja la información a través de las capas.

---

## 6. Reglas internas del proyecto

Reglas oficiales que rigen el desarrollo:

### **Naming conventions**

- Entidades: PascalCase  
- Repositorios: PascalCase + Repository  
- Interfaces: prefijo I  
- Casos de uso: PascalCase + UseCase  
- DTOs: PascalCase + DTO  
- Schemas: PascalCase + Request/Response  
- Archivos: snake_case  

### **Casos de uso**

- Una clase por caso de uso  
- Método público único: `execute()`  
- Sin lógica de infraestructura  
- Dependen solo de interfaces  
- Devuelven DTOs  

### **Entidades**

- Inmutables cuando sea posible  
- Sin Pydantic ni FastAPI  
- Validaciones internas  
- Representan conceptos del dominio  

### **Repositorios**

- Implementan interfaces en `shared/interfaces`  
- Devuelven entidades, no documentos Mongo  
- Usan mappers  
- Sin lógica de negocio  

### **Mappers**

- Funciones puras  
- Sin acceso a DB  
- Conocen estructura MongoDB  

### **DTOs**

- Solo en Application  
- Sin lógica  
- Convertibles a schemas  

### **Schemas Pydantic**

- Solo en API  
- Validación de entrada/salida  

### **Endpoints**

- Un router por recurso  
- Sin lógica de negocio  
- No acceden a DB directamente  

### **Errores**

- Dominio → domain/exceptions  
- Aplicación → shared_exceptions  
- HTTP → api/http_exceptions  
- Casos de uso no lanzan HTTPException  

### **Testing**

- Unit: dominio y casos de uso  
- Integration: repositorios reales  
- E2E: API completa con Docker  

### **PDF**

- Servicio en `infrastructure/pdf`  
- Interfaz `IPdfGenerator`  
- Plantillas HTML dedicadas  
- CSS separado del frontend  

### **Logging**

- Middlewares para requests, responses y tiempos  
- Handlers centralizados  
- Niveles por entorno  

### **Versionado**

- `/api/v1`  
- Cambios incompatibles → `/api/v2`  

### **Estructura de capas**

- API → Application → Domain → Infrastructure  
- Nunca saltarse capas  

---

## 7. Tecnologías clave

- Python 3.13  
- FastAPI 0.128  
- MongoDB (Motor async)  
- Pydantic 2.12  
- WeasyPrint  
- pytest + pytest-asyncio  
- Docker  
- Astro (frontend)  

---

## 8. Estado actual del proyecto

- **Backend:** En progreso  
  - Implementando: *EPIC 3.5 – Testing de integración y E2E*  
- **Frontend:** No iniciado  
- **Infraestructura:** Pendiente  
- **PDF:** Implementación planificada  

---

## 9. Milestones del proyecto

🟦 Milestone 1 — Análisis y Planificación
🟩 Milestone 2 — Diseño del Sistema
🟧 Milestone 3 — Implementación Backend (Clean Architecture)
🟧 Milestone 4 — Implementación Frontend (Astro + TypeScript + Tailwind CSS)
🟨 Milestone 5 — Pruebas (Backend + Frontend + E2E)
🟥 Milestone 6 — Despliegue (Backend + Frontend + Infraestructura)
🟪 Milestone 7 — Mantenimiento y Evolución

---

## 10. Estándares del proyecto

- **Black** → formateo  
- **Ruff** → linting  
- **isort** → orden de imports  
- **mypy** → tipado estático  
- **Bandit** → seguridad  
- **pre-commit** → hooks  

---

## 11. Versionado de API

- Todas las rutas bajo `/api/v1`  
- Futuras versiones: `/api/v2`, `/api/v3`…  
- Deprecación mediante headers HTTP  

---

## 12. Docker y entornos

- **dev:** recarga automática, logging detallado  
- **test:** DB efímera, datos controlados  
- **prod:** imágenes optimizadas, seguridad reforzada  

Docker garantiza entornos reproducibles y facilita CI/CD.

---

## 13. Configuración del sistema

Variables gestionadas con `pydantic-settings`:

ENVIRONMENT
API_HOST
API_PORT
MONGODB_URL
DATABASE_NAME
CORS_ORIGINS
SECRET_KEY

Entornos:

- `.env.development.local`  
- `.env.development.docker`  
- `.env.test`  

---

## 14. Objetivo final del proyecto

Construir un portfolio profesional que demuestre:

- Madurez técnica  
- Buenas prácticas  
- Arquitectura limpia  
- Código mantenible  
- Capacidad de diseño y ejecución de un proyecto completo  

---

## 15. Contacto

Este proyecto es parte del portfolio profesional de **Azfe**.
