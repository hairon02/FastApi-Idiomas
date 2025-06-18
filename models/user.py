from sqlalchemy import Column, Integer, String, Text
from db.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP as timestamp
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(255), unique=True)
    hashed_password = Column(Text)
    fecha_registro = Column(timestamp(timezone=True))

    # Relación uno-a-muchos con ProgresoLeccion
    progreso_lecciones = relationship("ProgresoLeccion", back_populates="usuario")
    # Relación uno-a-muchos con ProgresoVocabulario
    progreso_vocabulario = relationship("ProgresoVocabulario", back_populates="usuario")