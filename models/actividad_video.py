from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class ActividadVideo(Base):
    """
    Modelo SQLAlchemy para la tabla 'Actividad_Video'.
    Contenido específico para actividades de tipo 'VIDEO'.
    """
    __tablename__ = "actividad_video"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False, unique=True)
    id_video_youtube = Column(String(50), nullable=False)
    palabra_clave = Column(String(100))
    url_video_cloudinary = Column(Text)  # Aquí guardamos la URL del video subido

    # Relación uno-a-uno con Actividad
    actividad = relationship("Actividad", back_populates="actividad_video")