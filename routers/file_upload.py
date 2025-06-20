import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from routers.auth import get_current_user
from cloudinary.utils import cloudinary_url
from models.actividad_video import ActividadVideo
from db.database import get_db
from sqlalchemy.orm import Session

load_dotenv()  # Carga las variables de entorno desde un archivo .env
CLOUD_NAME = os.environ.get("CLOUD_NAME")
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

file_router = APIRouter(dependencies=[Depends(get_current_user)])

# Configuration       
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = API_KEY, 
    api_secret = API_SECRET, # Click 'View API Keys' above to copy your API secret
    secure=True
)


@file_router.post("/upload-file")
async def upload_file(actividad_video_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Leer el archivo en bytes
        file_bytes = await file.read()

        # Subir el archivo a Cloudinary (resource_type="auto" detecta imágenes, videos, etc)
        upload_result = cloudinary.uploader.upload(file_bytes, resource_type="auto")

        # Obtener URL segura del archivo subido
        url_publica = upload_result.get("secure_url")

        # Buscar la actividad asociada
        actividad_video = db.query(ActividadVideo).filter(ActividadVideo.id == actividad_video_id).first()

        if not url_publica:
            raise HTTPException(status_code=400, detail="No se pudo obtener la URL pública")

        if upload_result.get("resource_type") == "video":
            # Opcional: crear URL optimizada
            optimize_url, _ = cloudinary_url(
                upload_result["public_id"],
                resource_type="video",
                quality="auto"
            )
        else:
            optimize_url, _ = cloudinary_url(
                upload_result["public_id"],
                fetch_format="auto",
                quality="auto"
            )

        actividad_video.url_video_cloudinary = optimize_url
        db.commit()
        db.refresh(actividad_video)

        return {
            "public_id": upload_result["public_id"],
            "url": url_publica,
            "url_optimizada": optimize_url
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al subir archivo: {str(e)}")

