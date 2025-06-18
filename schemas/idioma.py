from typing import Optional
from pydantic import BaseModel, ConfigDict

class IdiomaBase(BaseModel):
    """
    Esquema base para un idioma.
    Define los atributos comunes para creación y lectura.
    """
    nombre: str
    codigo_iso: Optional[str] = None
    url_bandera: Optional[str] = None
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class IdiomaCreate(IdiomaBase):
    """
    Esquema para crear un nuevo idioma.
    Actualmente idéntico a IdiomaBase, pero puede añadir validaciones específicas.
    """
    pass

class IdiomaResponse(IdiomaBase):
    """
    Esquema para la respuesta de un idioma.
    Incluye el ID generado por la base de datos.
    """
    id: int


