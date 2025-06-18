from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.leccion import LeccionCreate, LeccionResponse
from models.leccion import Leccion

leccion = APIRouter()

@leccion.get("/lecciones", response_model=list[LeccionResponse])
async def get_lecciones(db: Session = Depends(get_db)):
    lecciones = db.query(Leccion).all()
    if not lecciones:
        raise HTTPException(status_code=404, detail="No se encontraron lecciones")
    return lecciones

@leccion.get("/lecciones/{leccion_id}", response_model=LeccionResponse)
async def get_leccion(leccion_id: int, db: Session = Depends(get_db)):
    leccion = db.query(Leccion).filter(Leccion.id == leccion_id).first()
    if not leccion:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    return leccion

@leccion.post("/lecciones", response_model=LeccionResponse)
async def create_leccion(leccion_create: LeccionCreate, db: Session = Depends(get_db)):
    existe = db.query(Leccion).filter(
        Leccion.id_nivel == leccion_create.id_nivel,
        Leccion.numero_leccion == leccion_create.numero_leccion
    ).first()
    if existe:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe una lección con el mismo nivel")
    new_leccion = Leccion(
        id_nivel=leccion_create.id_nivel,
        numero_leccion=leccion_create.numero_leccion,
        titulo=leccion_create.titulo,
        descripcion=leccion_create.descripcion
    )
    
    db.add(new_leccion)
    db.commit()
    db.refresh(new_leccion)
    return new_leccion