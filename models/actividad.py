from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.enums import TipoActividadEnum

class Actividad(Base):
    """
    Modelo SQLAlchemy para la tabla 'Actividades'.
    Define el orden y tipo de cada actividad en una lección.
    """
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True)
    id_leccion = Column(Integer, ForeignKey("lecciones.id", ondelete="CASCADE"), nullable=False)
    orden = Column(Integer, nullable=False)
    # Usa el tipo ENUM de PostgreSQL
    tipo_actividad = Column(ENUM(TipoActividadEnum, name="tipo_actividad_enum", create_type=False), nullable=False)

    # Restricción de unicidad para la combinación de id_leccion y orden
    __table_args__ = (UniqueConstraint('id_leccion', 'orden', name='uq_actividad_leccion_orden'),)

    # Relación muchos-a-uno con Leccion
    leccion = relationship("Leccion", back_populates="actividades")
    # Relaciones uno-a-uno con las tablas de contenido específico
    actividad_vocabulario = relationship("ActividadVocabulario", uselist=False, back_populates="actividad")
    actividad_oraciones = relationship("ActividadOracion", uselist=False, back_populates="actividad")
    actividad_video = relationship("ActividadVideo", uselist=False, back_populates="actividad")
    actividad_voz = relationship("ActividadVoz", uselist=False, back_populates="actividad")