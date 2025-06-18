from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base

class Leccion(Base):
    """
    Modelo SQLAlchemy para la tabla 'Lecciones'.
    Representa las lecciones dentro de cada nivel.
    """
    __tablename__ = "lecciones"

    id = Column(Integer, primary_key=True, index=True)
    id_nivel = Column(Integer, ForeignKey("niveles.id", ondelete="CASCADE"), nullable=False)
    numero_leccion = Column(Integer, nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)

    # Restricción de unicidad para la combinación de id_nivel y numero_leccion
    __table_args__ = (UniqueConstraint('id_nivel', 'numero_leccion', name='uq_leccion_nivel_numero'),)

    # Relación muchos-a-uno con Nivel
    nivel = relationship("Nivel", back_populates="lecciones")
    # Relación uno-a-muchos con Actividades
    actividades = relationship("Actividad", back_populates="leccion")
    # Relación muchos-a-muchos con Usuario a través de ProgresoLeccion
    progreso_lecciones = relationship("ProgresoLeccion", back_populates="leccion")
    