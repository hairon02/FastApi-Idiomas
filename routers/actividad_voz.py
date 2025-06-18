from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.actividad_voz import ActividadVoz
from schemas.actividad_voz import ActividadVozCreate, ActividadVozResponse
from db.database import get_db
from routers.auth import get_current_user

actividad_voz = APIRouter(dependencies=[Depends(get_current_user)])

@actividad_voz.get("/actividad_voz", response_model=list[ActividadVozResponse])
def read_actividad_voz_list(db: Session = Depends(get_db)):
    db_actividad_voz = db.query(ActividadVoz).all()
    if not db_actividad_voz:
        raise HTTPException(status_code=404, detail="No se encontraron actividades de voz")
    return db_actividad_voz

@actividad_voz.get("/actividad_voz/{actividad_voz_id}", response_model=ActividadVozResponse)
def read_actividad_voz(actividad_voz_id: int, db: Session = Depends(get_db)):
    db_actividad_voz = db.query(ActividadVoz).filter(ActividadVoz.id == actividad_voz_id).first()
    if not db_actividad_voz:
        raise HTTPException(status_code=404, detail="Actividad de voz no encontrada")
    return db_actividad_voz

@actividad_voz.post("/actividad_voz/", response_model=ActividadVozResponse)
def create_actividad_voz(
    actividad_voz: ActividadVozCreate, db: Session = Depends(get_db)
):
    existe = db.query(ActividadVoz).filter(
        ActividadVoz.id_actividad == actividad_voz.id_actividad
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una actividad de voz con el mismo ID de actividad")
    db_actividad_voz = ActividadVoz(**actividad_voz.model_dump())
    db.add(db_actividad_voz)
    db.commit()
    db.refresh(db_actividad_voz)
    return db_actividad_voz