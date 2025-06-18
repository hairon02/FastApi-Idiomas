from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.actividad_vocabulario import ActividadVocabulario
from schemas.actividad_vocabulario import ActividadVocabularioCreate, ActividadVocabularioResponse
from db.database import get_db

actividad_vocabulario = APIRouter()

@actividad_vocabulario.get("/actividad_vocabulario", response_model=list[ActividadVocabularioResponse])
def read_actividad_vocabulario_list(db: Session = Depends(get_db)):
    db_actividad_vocabulario = db.query(ActividadVocabulario).all()
    if not db_actividad_vocabulario:
        raise HTTPException(status_code=404, detail="No se encontraron actividades de vocabulario")
    return db_actividad_vocabulario

@actividad_vocabulario.get("/actividad_vocabulario/{actividad_vocabulario_id}", response_model=ActividadVocabularioResponse)
def read_actividad_vocabulario(actividad_vocabulario_id: int, db: Session = Depends(get_db)):
    db_actividad_vocabulario = db.query(ActividadVocabulario).filter(ActividadVocabulario.id == actividad_vocabulario_id).first()
    if not db_actividad_vocabulario:
        raise HTTPException(status_code=404, detail="Actividad de vocabulario no encontrada")
    return db_actividad_vocabulario

@actividad_vocabulario.post("/actividad_vocabulario/", response_model=ActividadVocabularioResponse)
def create_actividad_vocabulario(
    actividad_vocabulario: ActividadVocabularioCreate, db: Session = Depends(get_db)
):
    existe = db.query(ActividadVocabulario).filter(
        ActividadVocabulario.id_actividad == actividad_vocabulario.id_actividad
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una actividad de vocabulario con el mismo ID de actividad")
    db_actividad_vocabulario = ActividadVocabulario(**actividad_vocabulario.model_dump())
    db.add(db_actividad_vocabulario)
    db.commit()
    db.refresh(db_actividad_vocabulario)
    return db_actividad_vocabulario