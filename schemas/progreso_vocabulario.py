from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enums import EstadoVocabEnum

class ProgresoVocabularioBase(BaseModel):
    """
    Esquema base para Progreso_Vocabulario.
    """
    id_usuario: int # Cambiado de UUID a int
    id_palabra: int
    estado_aprendizaje: EstadoVocabEnum = EstadoVocabEnum.NUEVA
    aciertos: int = 0
    fallos: int = 0
    fecha_ultimo_repaso: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ProgresoVocabularioCreate(ProgresoVocabularioBase):
    """
    Esquema para crear un nuevo registro de progreso de vocabulario.
    """
    pass

class ProgresoVocabularioResponse(ProgresoVocabularioBase):
    """
    Esquema para la respuesta de progreso de vocabulario.
    """
    # usuario: Optional[UsuarioResponse] = None
    # palabra_vocabulario: Optional[ActividadVocabularioResponse] = None
