from pydantic import BaseModel, ConfigDict
from typing import Optional

# Niveles
class NivelBase(BaseModel):
    """
    Esquema base para un nivel.
    """
    id_idioma: int
    numero_nivel: int
    titulo: str
    descripcion: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class NivelCreate(NivelBase):
    """
    Esquema para crear un nuevo nivel.
    """
    pass

class NivelResponse(NivelBase):
    """
    Esquema para la respuesta de un nivel.
    """
    id: int
    # Puedes anidar el esquema del idioma si quieres incluir la información completa del idioma
    # idioma: Optional[IdiomaResponse] = None

