from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.actividad import ActividadCreate, ActividadResponse
from models.actividad import Actividad
from db.database import get_db

actividad = APIRouter()

@actividad.get("/actividades", response_model=list[ActividadResponse])
async def get_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividad).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No se encontraron actividades")
    return actividades

@actividad.post("/actividades", response_model=ActividadResponse)
async def create_actividad(actividad_create: ActividadCreate, db: Session = Depends(get_db)):
    existe = db.query(Actividad).filter(
        Actividad.id_leccion == actividad_create.id_leccion,
        Actividad.orden == actividad_create.orden
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una actividad con el mismo orden en esta lección")
    nueva_actividad = Actividad(**actividad_create.model_dump())
    db.add(nueva_actividad)
    db.commit()
    db.refresh(nueva_actividad)
    return nueva_actividad

@actividad.get("/actividades/{actividad_id}", response_model=ActividadResponse)
async def get_actividad(actividad_id: int, db: Session = Depends(get_db)):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad