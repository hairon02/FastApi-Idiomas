from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.actividad_video import ActividadVideo
from schemas.actividad_video import ActividadVideoCreate, ActividadVideoResponse
from db.database import get_db
from routers.auth import get_current_user
actividad_video = APIRouter(dependencies=[Depends(get_current_user)])

@actividad_video.get("/actividad_video", response_model=list[ActividadVideoResponse])
def read_actividad_oracion_list(db: Session = Depends(get_db)):
    db_actividad_oracion = db.query(ActividadVideo).all()
    if not db_actividad_oracion:
        raise HTTPException(status_code=404, detail="No Actividad Oracion found")
    return db_actividad_oracion

@actividad_video.get("/actividad_video/{actividad_oracion_id}", response_model=ActividadVideoResponse)
def read_actividad_oracion(actividad_oracion_id: int, db: Session = Depends(get_db)):
    db_actividad_oracion = db.query(ActividadVideo).filter(ActividadVideo.id == actividad_oracion_id).first()
    if not db_actividad_oracion:
        raise HTTPException(status_code=404, detail="Actividad Oracion not found")
    return db_actividad_oracion

@actividad_video.post("/actividad_video/", response_model=ActividadVideoResponse)
def create_actividad_oracion(
    actividad_video: ActividadVideoCreate, db: Session = Depends(get_db)
):
    existe = db.query(ActividadVideo).filter(
        ActividadVideo.id_actividad == actividad_video.id_actividad
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una actividad de oración con el mismo ID de actividad")
    db_actividad_oracion = ActividadVideo(**actividad_video.model_dump())
    db.add(db_actividad_oracion)
    db.commit()
    db.refresh(db_actividad_oracion)
    return db_actividad_oracion