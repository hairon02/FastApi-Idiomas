from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from db.database import Base

class ActividadVideo(Base):
    __tablename__ = "actividad_video"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False, unique=True)
    id_video_youtube = Column(String(50), nullable=False)
    descripcion = Column(Text)
    pregunta = Column(Text)
    opciones = Column(JSONB)
    respuesta_correcta = Column(Text)

    actividad = relationship("Actividad", back_populates="actividad_video")