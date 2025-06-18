from pydantic import BaseModel, ConfigDict
from typing import Optional

# Lecciones
class LeccionBase(BaseModel):
    """
    Esquema base para una lección.
    """
    id_nivel: int
    numero_leccion: int
    titulo: str
    descripcion: Optional[str] = None

class LeccionCreate(LeccionBase):
    """
    Esquema para crear una nueva lección.
    """
    pass

class LeccionResponse(LeccionBase):
    """
    Esquema para la respuesta de una lección.
    """
    id: int
    # nivel: Optional[NivelResponse] = None

    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )
