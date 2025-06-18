from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Idioma(Base):
    """
    Modelo SQLAlchemy para la tabla 'Idiomas'.
    Almacena los idiomas disponibles en la aplicación.
    """
    __tablename__ = "idiomas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    codigo_iso = Column(String(10), unique=True)
    url_bandera = Column(String(255))

    # Relación uno-a-muchos con Niveles
    niveles = relationship("Nivel", back_populates="idioma")




