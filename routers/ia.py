from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from services.ia_services import explicar_error_con_prompt
from routers.auth import get_current_user

ia_router = APIRouter(dependencies=[Depends(get_current_user)])

class ExplicarErrorRequest(BaseModel):
    error_usuario: str
    idioma: str = "español"  # Valor por defecto (puede cambiarse en el request)

    model_config = ConfigDict(
        from_attributes=True
    )


@ia_router.post("/explicar-error")
def explicar_error_usuario(request: ExplicarErrorRequest):
    explicacion = explicar_error_con_prompt(request.error_usuario, request.idioma)
    return {"explicacion": explicacion}