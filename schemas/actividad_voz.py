from pydantic import BaseModel, ConfigDict

class ActividadVozBase(BaseModel):
    """
    Esquema base para Actividad_Voz.
    """
    id_actividad: int
    frase_a_repetir: str
    
    model_config = ConfigDict(
        from_attributes = True # Para Pydantic v2+ (anteriormente orm_mode = True)
    )

class ActividadVozCreate(ActividadVozBase):
    pass

class ActividadVozResponse(ActividadVozBase):
    id: int
    # actividad: Optional[ActividadResponse] = None
