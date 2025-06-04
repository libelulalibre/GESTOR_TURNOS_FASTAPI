from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.profesional import ProfesionalCreate, ProfesionalInDB
from app.schemas.turno import ConfiguracionCentroCreate, ConfiguracionCentroInDB
from app.services.profesional_service import create_profesional, get_profesionales
from app.services.admin_service import (
    create_configuracion_centro,
    get_configuracion_centro,
    update_configuracion_centro,
)
from app.database.session import get_db
from app.utils.security import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

@router.post("/profesionales/", response_model=ProfesionalInDB)
def crear_profesional(
    profesional: ProfesionalCreate,
    db: Session = Depends(get_db)
):
    return create_profesional(db, profesional)

@router.get("/profesionales/", response_model=List[ProfesionalInDB])
def listar_profesionales(db: Session = Depends(get_db)):
    return get_profesionales(db)

@router.post("/configuracion/", response_model=ConfiguracionCentroInDB)
def crear_configuracion_centro(
    config: ConfiguracionCentroCreate,
    db: Session = Depends(get_db)
):
    return create_configuracion_centro(db, config)

@router.get("/configuracion/", response_model=ConfiguracionCentroInDB)
def obtener_configuracion_centro(db: Session = Depends(get_db)):
    config = get_configuracion_centro(db)
    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return config

@router.put("/configuracion/", response_model=ConfiguracionCentroInDB)
def actualizar_configuracion_centro(
    config: ConfiguracionCentroCreate,
    db: Session = Depends(get_db)
):
    return update_configuracion_centro(db, config)