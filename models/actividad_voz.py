from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class ActividadVoz(Base):
    """
    Modelo SQLAlchemy para la tabla 'Actividad_Voz'.
    Contenido específico para actividades de tipo 'VOZ'.
    """
    __tablename__ = "actividad_voz"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False, unique=True)
    frase_a_repetir = Column(Text, nullable=False)

    # Relación uno-a-uno con Actividad
    actividad = relationship("Actividad", back_populates="actividad_voz")