from pydantic import BaseModel
from datetime import datetime

class TurnoBase(BaseModel):
    usuario_id: int
    profesional_id: int
    fecha: datetime.date  # o datetime.datetime
    hora: datetime.time

class TurnoCreate(TurnoBase):
    pass

class TurnoResponse(TurnoBase):
    id: int
    estado: str
    especialidad: str
    
    class Config:
        orm_mode = True