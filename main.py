from fastapi import FastAPI
from app.routers import turnos
from app.database.session import engine
from app.database.base import Base

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

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)