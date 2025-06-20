# models/idioma.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Idioma(Base):
    __tablename__ = "idiomas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    codigo_iso = Column(String(10), unique=True)
    url_bandera = Column(String(255))
    url_fondo_curso = Column(String(255)) # <-- AÑADE ESTA LÍNEA

    niveles = relationship("Nivel", back_populates="idioma")
