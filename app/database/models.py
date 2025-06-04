from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Date, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    telefono = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    rol = Column(String)  # "usuario", "profesional", "admin"
    
    turnos = relationship("Turno", back_populates="usuario")

class Profesional(Base):
    __tablename__ = "profesionales"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    especialidad = Column(String)
    matricula = Column(String, unique=True)
    
    usuario = relationship("Usuario")
    horarios = relationship("HorarioProfesional", back_populates="profesional")
    turnos = relationship("Turno", back_populates="profesional")

class HorarioProfesional(Base):
    __tablename__ = "horarios_profesionales"
    
    id = Column(Integer, primary_key=True, index=True)
    profesional_id = Column(Integer, ForeignKey("profesionales.id"))
    dia_semana = Column(Integer)  # 0-6 (lunes-domingo)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    
    profesional = relationship("Profesional", back_populates="horarios")

class Turno(Base):
    __tablename__ = "turnos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    profesional_id = Column(Integer, ForeignKey("profesionales.id"))
    fecha = Column(Date)
    hora = Column(Time)
    estado = Column(String, default="pendiente")  # "pendiente", "confirmado", "cancelado", "completado"
    motivo = Column(String)
    especialidad = Column(String)  # Nueva columna añadida
    
    # Relaciones actualizadas
    usuario = relationship("Usuario", back_populates="turnos")
    profesional = relationship("Profesional", back_populates="turnos")

    # Método para convertir a diccionario (útil para responses)
    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora": self.hora.isoformat() if self.hora else None,
            "estado": self.estado,
            "especialidad": self.especialidad,
            "profesional_id": self.profesional_id,
            "usuario_id": self.usuario_id
        }

class ConfiguracionCentro(Base):
    __tablename__ = "configuracion_centro"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_centro = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)
    horario_apertura = Column(Time)
    horario_cierre = Column(Time)
    dias_atencion = Column(String)  # "0,1,2,3,4" para lunes a viernes
    duracion_turno = Column(Integer, default=30)  # Nueva columna en minutos