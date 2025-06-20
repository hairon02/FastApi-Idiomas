from typing import Optional
from pydantic import BaseModel, ConfigDict

class ActividadVideoBase(BaseModel):
    """
    Esquema base para Actividad_Video.
    """
    id_actividad: int
    id_video_youtube: str
    palabra_clave: Optional[str] = None
    url_video_cloudinary: Optional[str] = None
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ActividadVideoCreate(ActividadVideoBase):
    pass

class ActividadVideoResponse(ActividadVideoBase):
    id: int
    # actividad: Optional[ActividadResponse] = None

