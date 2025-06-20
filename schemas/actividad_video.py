from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class ActividadVideoBase(BaseModel):
    id_actividad: int
    id_video_youtube: str
    descripcion: Optional[str] = None
    pregunta: Optional[str] = None
    opciones: Optional[List[str]] = None
    respuesta_correcta: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ActividadVideoCreate(ActividadVideoBase):
    pass

class ActividadVideoResponse(ActividadVideoBase):
    id: int