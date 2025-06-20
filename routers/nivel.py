from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.nivel import Nivel
from schemas.nivel import NivelCreate, NivelResponse
from schemas.user import UserResponse  # Importante añadir
from sqlalchemy import or_
from routers.auth import get_current_user

# Quitamos la dependencia de aquí y movemos el tag
nivel = APIRouter(prefix="/niveles", tags=["niveles"])

@nivel.get("/", response_model=list[NivelResponse])
# Añadimos la dependencia aquí
async def get_niveles(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    niveles = db.query(Nivel).all()
    if not niveles:
        raise HTTPException(status_code=404, detail="No se encontraron niveles")
    return niveles

@nivel.get("/{nivel_id}", response_model=NivelResponse)
# Añadimos la dependencia aquí
async def get_nivel(nivel_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    nivel = db.query(Nivel).filter(Nivel.id == nivel_id).first()
    if not nivel:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel

@nivel.post("/", response_model=NivelResponse)
# Añadimos la dependencia aquí
async def create_nivel(nivel_create: NivelCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    existe = db.query(Nivel).filter(
        Nivel.id_idioma == nivel_create.id_idioma,
        Nivel.numero_nivel == nivel_create.numero_nivel
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe ese nivel con el mismo id_idioma")
    
    new_nivel = Nivel(**nivel_create.model_dump())
    db.add(new_nivel)
    db.commit()
    db.refresh(new_nivel)
    return new_nivel