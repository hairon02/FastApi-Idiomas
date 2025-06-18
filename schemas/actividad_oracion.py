from typing import List
from pydantic import BaseModel, ConfigDict

class ActividadOracionBase(BaseModel):
    """
    Esquema base para Actividad_Oraciones.
    """
    id_actividad: int
    frase_correcta: str
    banco_palabras: List[str] # Asumiendo que es una lista de strings para el JSONB
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ActividadOracionCreate(ActividadOracionBase):
    pass

class ActividadOracionResponse(ActividadOracionBase):
    id: int
    # actividad: Optional[ActividadResponse] = None
