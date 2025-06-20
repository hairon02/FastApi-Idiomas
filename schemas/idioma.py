# schemas/idioma.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

class IdiomaBase(BaseModel):
    nombre: str
    codigo_iso: Optional[str] = None
    url_bandera: Optional[str] = None
    url_fondo_curso: Optional[str] = None # <-- AÑADE ESTA LÍNEA
    model_config = ConfigDict(from_attributes=True)

class IdiomaCreate(IdiomaBase):
    pass

class IdiomaResponse(IdiomaBase):
    id: int