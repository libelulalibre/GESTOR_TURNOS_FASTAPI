from fastapi import FastAPI
from app.routers import turnos  # Importa el router de turnos

# Crea la instancia de FastAPI
app = FastAPI(
    title="Gestor de Turnos API",
    description="API para gestión de turnos médicos",
    version="0.1.0"
)

# Incluye el router de turnos
app.include_router(turnos.router)
app.include_router(auth.router, prefix="/auth")

# Endpoint básico de prueba
@app.get("/")
def home():
    return {"message": "Bienvenido al Gestor de Turnos"}
