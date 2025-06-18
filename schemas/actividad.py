from pydantic import BaseModel, ConfigDict
from schemas.enums import TipoActividadEnum


# Actividades
class ActividadBase(BaseModel):
    """
    Esquema base para una actividad.
    """
    id_leccion: int
    orden: int
    tipo_actividad: TipoActividadEnum # Usa el Enum de Python
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ActividadCreate(ActividadBase):
    """
    Esquema para crear una nueva actividad.
    """
    pass

class ActividadResponse(ActividadBase):
    """
    Esquema para la respuesta de una actividad.
    """
    id: int
    # leccion: Optional[LeccionResponse] = None

