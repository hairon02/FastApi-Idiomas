# routers/audio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.actividad_vocabulario import ActividadVocabulario
from services.ia_services import generar_audio_desde_texto
from fastapi.responses import StreamingResponse
import io

audio_router = APIRouter(prefix="/audio", tags=["audio"])

@audio_router.get("/vocabulario/{id_palabra}")
def obtener_audio_vocabulario(id_palabra: int, db: Session = Depends(get_db)):
    detalle_vocabulario = db.query(ActividadVocabulario).filter(ActividadVocabulario.id == id_palabra).first()
    if not detalle_vocabulario:
        raise HTTPException(status_code=404, detail="Palabra de vocabulario no encontrada")

    audio_bytes = generar_audio_desde_texto(texto=detalle_vocabulario.palabra, codigo_idioma="pt-BR")

    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")