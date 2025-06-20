# En el archivo: routers/ia.py

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from services.ia_services import explicar_error_con_prompt, transcribir_audio_a_texto
from schemas.user import UserResponse
from routers.auth import get_current_user
from db.database import get_db
from sqlalchemy.orm import Session
from services.ia_services import verificar_similitud_frase
from models.actividad_voz import ActividadVoz


# Aplicamos el mismo patrón de prefijo para mantener el código organizado
ia_router = APIRouter(prefix="/ia", tags=["IA"])

# --- Endpoint para explicar errores (el que ya tenías) ---
class ExplicarErrorRequest(BaseModel):
    error_usuario: str
    idioma: str = "español"

@ia_router.post("/explicar-error")
def explicar_error_usuario(
    request: ExplicarErrorRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    explicacion = explicar_error_con_prompt(request.error_usuario, request.idioma)
    return {"explicacion": explicacion}


# --- NUEVO ENDPOINT PARA TRANSCRIBIR AUDIO ---
@ia_router.post("/transcribir-audio")
async def transcribir_audio(
    audio_file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user)
):
    # Leemos los bytes del archivo de audio que nos envió Flutter
    audio_bytes = await audio_file.read()

    # Llamamos a nuestro servicio para que lo envíe a la API de Google
    # TODO: En el futuro, el código de idioma podría venir en la petición
    transcripcion = transcribir_audio_a_texto(audio_bytes, "pt-BR")

    # Devolvemos el texto transcrito a Flutter
    return {"transcripcion": transcripcion}

class VerificarVozRequest(BaseModel):
    id_actividad_voz: int
    transcripcion_usuario: str

# --- AÑADE ESTE NUEVO ENDPOINT ---
@ia_router.post("/verificar-voz")
def verificar_respuesta_voz(
    request: VerificarVozRequest,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    # 1. Buscar la frase correcta en la base de datos
    actividad = db.query(ActividadVoz).filter(ActividadVoz.id == request.id_actividad_voz).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad de voz no encontrada")

    # 2. Usar nuestro servicio para comparar las frases
    es_correcta = verificar_similitud_frase(
        frase_usuario=request.transcripcion_usuario,
        frase_correcta=actividad.frase_a_repetir
    )

    # 3. Devolver el resultado a Flutter
    return {"es_correcta": es_correcta}