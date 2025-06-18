from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.idioma import Idioma
from schemas.idioma import IdiomaResponse, IdiomaCreate
from sqlalchemy import or_
from routers.auth import get_current_user

idioma = APIRouter(dependencies=[Depends(get_current_user)])

@idioma.get("/idiomas", response_model=list[IdiomaResponse])
async def get_idiomas(db: Session = Depends(get_db)):
    idiomas = db.query(Idioma).all()
    if not idiomas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No idiomas found")
    return idiomas

@idioma.get("/idiomas/{idioma_id}", response_model=IdiomaResponse)
async def get_idioma(idioma_id: int, db: Session = Depends(get_db)):
    idioma = db.query(Idioma).filter(Idioma.id == idioma_id).first()
    if not idioma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idioma not found")
    return idioma

@idioma.post("/idiomas", response_model=IdiomaResponse)
async def create_idioma(idioma: IdiomaCreate, db: Session = Depends(get_db)):
    # Verificar si el idioma ya existe
    existing_idioma = db.query(Idioma).filter(or_(Idioma.nombre == idioma.nombre, Idioma.codigo_iso == idioma.codigo_iso) ).first()
    if existing_idioma.nombre == idioma.nombre:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El idioma ya existe")
    elif existing_idioma.codigo_iso == idioma.codigo_iso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código ISO ya está en uso")
    new_idioma = Idioma(
        nombre=idioma.nombre,
        codigo_iso=idioma.codigo_iso,
        url_bandera=idioma.url_bandera
    )
    db.add(new_idioma)
    db.commit()
    db.refresh(new_idioma)
    return new_idioma