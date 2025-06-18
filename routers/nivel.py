from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.nivel import Nivel
from schemas.nivel import NivelCreate, NivelResponse
from sqlalchemy import or_
from routers.auth import get_current_user

nivel = APIRouter(dependencies=[Depends(get_current_user)])

@nivel.get("/niveles", response_model=list[NivelResponse])
async def get_niveles(db: Session = Depends(get_db)):
    niveles = db.query(Nivel).all()
    if not niveles:
        raise HTTPException(status_code=404, detail="No se encontraron niveles")
    return niveles

@nivel.get("/niveles/{nivel_id}", response_model=NivelResponse)
async def get_nivel(nivel_id: int, db: Session = Depends(get_db)):
    nivel = db.query(Nivel).filter(Nivel.id == nivel_id).first()
    if not nivel:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel

@nivel.post("/niveles", response_model=NivelResponse)
async def create_nivel(nivel_create: NivelCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un nivel con el mismo id_idioma y numero_nivel
    existe = db.query(Nivel).filter(
        Nivel.id_idioma == nivel_create.id_idioma,
        Nivel.numero_nivel == nivel_create.numero_nivel
    ).first()
    print(existe)
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe ese nivel con el mismo id_idioma")
    new_nivel = Nivel(
        id_idioma=nivel_create.id_idioma,
        numero_nivel=nivel_create.numero_nivel,
        titulo=nivel_create.titulo,
        descripcion=nivel_create.descripcion
    )
    
    db.add(new_nivel)
    db.commit()
    db.refresh(new_nivel)
    return new_nivel