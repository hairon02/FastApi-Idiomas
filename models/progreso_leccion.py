from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.enums import EstadoLeccionEnum


class ProgresoLeccion(Base):
    """
    Modelo SQLAlchemy para la tabla 'Progreso_Lecciones'.
    Rastrea el progreso de los usuarios en las lecciones.
    """
    __tablename__ = "Progreso_Lecciones"

    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_leccion = Column(Integer, ForeignKey("lecciones.id", ondelete="CASCADE"), primary_key=True)
    # Usa el tipo ENUM de PostgreSQL
    estado = Column(ENUM(EstadoLeccionEnum, name="estado_leccion_enum", create_type=False), nullable=False, default=EstadoLeccionEnum.NO_INICIADA)
    ultima_actividad = Column(Integer, nullable=False, default=0)
    fecha_ultimo_acceso = Column(TIMESTAMP(timezone=True), default=func.now())
    puntuacion_alta = Column(Integer, default=0)

    # Relación muchos-a-uno con Usuario
    usuario = relationship("User", back_populates="progreso_lecciones")
    # Relación muchos-a-uno con Leccion
    leccion = relationship("Leccion", back_populates="progreso_lecciones")
    # “La tabla Lecciones debe tener una propiedad llamada progreso_lecciones.”