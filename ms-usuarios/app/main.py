from fastapi import FastAPI

# El root_path hace la magia: le avisa a Swagger UI que estamos detrás de un Gateway
app = FastAPI(
    title="Microservicio de Usuarios",
    root_path="/api/usuarios"
)

# Nota que aquí dejamos la ruta limpia, sin el prefijo
@app.get("/get-usuarios")
def obtener_usuarios():
    """Endpoint principal que Traefik enrutará."""
    return {
        "status": "success",
        "message": "¡Hola desde el MS de Usuarios!",
        "data": [
            {"id": 1, "nombre": "Dev 1"},
            {"id": 2, "nombre": "Dev 2"}
        ]
    }
    
@app.get("/health")
def health_check():
    """Endpoint vital para el monitoreo."""
    return {"status": "ok", "service": "ms-usuarios"}