from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.turno import TurnoCreate, TurnoResponse
from app.database.models import Turno, Usuario, Profesional

router = APIRouter(prefix="/turnos", tags=["turnos"])

@router.post("/", response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
async def crear_turno(turno_data: TurnoCreate, db: Session = Depends(get_db)):
    # Verificar si existe el usuario
    usuario = db.query(Usuario).filter(Usuario.id == turno_data.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar si existe el profesional
    profesional = db.query(Profesional).filter(Profesional.id == turno_data.profesional_id).first()
    if not profesional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesional no encontrado"
        )
    
    # Verificar disponibilidad del turno (aquí deberías implementar tu lógica específica)
    turno_existente = db.query(Turno).filter(
        Turno.profesional_id == turno_data.profesional_id,
        Turno.fecha == turno_data.fecha,
        Turno.hora == turno_data.hora
    ).first()
    
    if turno_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un turno en ese horario"
        )
    
    # Crear el nuevo turno
    nuevo_turno = Turno(
        usuario_id=turno_data.usuario_id,
        profesional_id=turno_data.profesional_id,
        fecha=turno_data.fecha,
        hora=turno_data.hora,
        estado="pendiente",
        motivo=turno_data.motivo,
        especialidad=profesional.especialidad  # Tomamos la especialidad del profesional
    )
    
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    
    return nuevo_turno

@router.get("/{turno_id}", response_model=TurnoResponse)
async def obtener_turno(turno_id: int, db: Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turno no encontrado"
        )
    
    return turno