from fastapi import FastAPI

app = FastAPI()

# Datos de ejemplo: reemplázalos por tus experiencias reales
experiences = [
    {
        "company": "Arttalo Tech | for SEAT & CUPRA",
        "role": "Desarrollador Backend",
        "location": "Martorell",
        "years": "2021-2025",
        "description": "• Traducción de diseños a código.\n• Optimización de la Experiencia de Usuario (UX).\n• Desarrollo de interfaces responsivas y accesibles.\n• Optimización de rendimiento frontend.\n• Implementación de microinteracciones y animaciones.\n• Colaboración con equipos multidisciplinarios."
    },
    {
        "company": "Empresa B",
        "role": "Ingeniero de Software",
        "location": "Martorell",
        "years": "2019-2021",
        "description": """• Desarrollo de APIs con Python.
• Integración con servicios externos.
• Optimización de rendimiento."""
    }
]

@app.get("/cv/experience")
def get_experience():
    return experiences
