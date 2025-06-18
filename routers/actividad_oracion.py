from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.actividad_oracion import ActividadOracion
from schemas.actividad_oracion import ActividadOracionCreate, ActividadOracionResponse
from db.database import get_db
from routers.auth import get_current_user

actividad_oracion = APIRouter(dependencies=[Depends(get_current_user)])

@actividad_oracion.get("/actividad_oracion", response_model=list[ActividadOracionResponse])
def read_actividad_oracion_list(db: Session = Depends(get_db)):
    db_actividad_oracion = db.query(ActividadOracion).all()
    if not db_actividad_oracion:
        raise HTTPException(status_code=404, detail="No Actividad Oracion found")
    return db_actividad_oracion


@actividad_oracion.get("/actividad_oracion/{actividad_oracion_id}", response_model=ActividadOracionResponse)
def read_actividad_oracion(actividad_oracion_id: int, db: Session = Depends(get_db)):
    db_actividad_oracion = db.query(ActividadOracion).filter(ActividadOracion.id == actividad_oracion_id).first()
    if not db_actividad_oracion:
        raise HTTPException(status_code=404, detail="Actividad Oracion not found")
    return db_actividad_oracion


@actividad_oracion.post("/actividad_oracion/", response_model=ActividadOracionResponse)
def create_actividad_oracion(
    actividad_oracion: ActividadOracionCreate, db: Session = Depends(get_db)
):
    existe = db.query(ActividadOracion).filter(
        ActividadOracion.id_actividad == actividad_oracion.id_actividad
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una actividad de oración con el mismo ID de actividad")
    db_actividad_oracion = ActividadOracion(**actividad_oracion.dict())
    db.add(db_actividad_oracion)
    db.commit()
    db.refresh(db_actividad_oracion)
    return db_actividad_oracion