from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.enums import EstadoVocabEnum

class ProgresoVocabulario(Base):
    """
    Modelo SQLAlchemy para la tabla 'Progreso_Vocabulario'.
    Rastrea el progreso de los usuarios con cada palabra del vocabulario.
    """
    __tablename__ = "Progreso_Vocabulario"

    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_palabra = Column(Integer, ForeignKey("Actividad_Vocabulario.id", ondelete="CASCADE"), primary_key=True)
    # Usa el tipo ENUM de PostgreSQL
    estado_aprendizaje = Column(ENUM(EstadoVocabEnum, name="estado_vocab_enum", create_type=False), nullable=False, default=EstadoVocabEnum.NUEVA)
    aciertos = Column(Integer, nullable=False, default=0)
    fallos = Column(Integer, nullable=False, default=0)
    fecha_ultimo_repaso = Column(TIMESTAMP(timezone=True)) # Puede ser nulo si no se ha repasado

    # Relación muchos-a-uno con Usuario
    usuario = relationship("User", back_populates="progreso_vocabulario")
    # Relación muchos-a-uno con ActividadVocabulario
    palabra_vocabulario = relationship("ActividadVocabulario", back_populates="progreso_usuarios")
