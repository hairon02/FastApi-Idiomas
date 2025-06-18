from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class ActividadOracion(Base):
    """
    Modelo SQLAlchemy para la tabla 'Actividad_Oraciones'.
    Contenido específico para actividades de tipo 'ORACION'.
    """
    __tablename__ = "actividad_oraciones"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False, unique=True)
    frase_correcta = Column(Text, nullable=False)
    # JSONB para almacenar datos JSON, aquí una lista de palabras
    banco_palabras = Column(JSONB, nullable=False)

    # Relación uno-a-uno con Actividad
    actividad = relationship("Actividad", back_populates="actividad_oraciones")