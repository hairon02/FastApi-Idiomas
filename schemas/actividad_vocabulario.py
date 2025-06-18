from pydantic import BaseModel, ConfigDict
from typing import Optional

class ActividadVocabularioBase(BaseModel):
    """
    Esquema base para Actividad_Vocabulario.
    """
    id_actividad: int
    palabra: str
    traduccion: str
    url_audio: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ActividadVocabularioCreate(ActividadVocabularioBase):
    pass

class ActividadVocabularioResponse(ActividadVocabularioBase):
    id: int
    # actividad: Optional[ActividadResponse] = None
