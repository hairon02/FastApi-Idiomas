from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class ActividadVocabulario(Base):
    """
    Modelo SQLAlchemy para la tabla 'Actividad_Vocabulario'.
    Contenido específico para actividades de tipo 'VOCABULARIO'.
    """
    __tablename__ = "Actividad_Vocabulario"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False, unique=True)
    palabra = Column(String(100), nullable=False)
    traduccion = Column(String(100), nullable=False)
    url_audio = Column(String(255))

    # Relación uno-a-uno con Actividad
    actividad = relationship("Actividad", back_populates="actividad_vocabulario")
    # Relación uno-a-muchos con ProgresoVocabulario (muchos usuarios pueden tener progreso sobre esta palabra)
    progreso_usuarios = relationship("ProgresoVocabulario", back_populates="palabra_vocabulario")