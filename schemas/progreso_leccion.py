from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enums import EstadoLeccionEnum

class ProgresoLeccionBase(BaseModel):
    """
    Esquema base para Progreso_Lecciones.
    """
    id_usuario: int # Cambiado de UUID a int
    id_leccion: int
    estado: EstadoLeccionEnum = EstadoLeccionEnum.NO_INICIADA
    ultima_actividad: int = 0
    puntuacion_alta: int = 0
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ProgresoLeccionCreate(ProgresoLeccionBase):
    """
    Esquema para crear un nuevo registro de progreso de lección.
    Los campos con default pueden omitirse en la creación.
    """
    pass

class ProgresoLeccionResponse(ProgresoLeccionBase):
    """
    Esquema para la respuesta de progreso de lección.
    Incluye fecha_ultimo_acceso.
    """
    fecha_ultimo_acceso: datetime
    # usuario: Optional[UsuarioResponse] = None
    # leccion: Optional[LeccionResponse] = None

