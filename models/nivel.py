from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base

class Nivel(Base):
    """
    Modelo SQLAlchemy para la tabla 'Niveles'.
    Representa los niveles de cada idioma.
    """
    __tablename__ = "niveles"

    id = Column(Integer, primary_key=True, index=True)
    id_idioma = Column(Integer, ForeignKey("idiomas.id", ondelete="CASCADE"), nullable=False)
    numero_nivel = Column(Integer, nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)

    # Restricción de unicidad para la combinación de id_idioma y numero_nivel
    __table_args__ = (UniqueConstraint('id_idioma', 'numero_nivel', name='uq_nivel_idioma_numero'),)

    # Relación muchos-a-uno con Idioma
    idioma = relationship("Idioma", back_populates="niveles")
    # Relación uno-a-muchos con Lecciones
    lecciones = relationship("Leccion", back_populates="nivel")