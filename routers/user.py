# En routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.idioma import Idioma
from schemas.user import SelectLanguageRequest, UserCreate, UserResponse # Importamos los nuevos esquemas
from models.user import User
from db.database import get_db
from routers.auth import get_password_hash, get_current_user
from datetime import datetime

user = APIRouter()

@user.post("/users", response_model=UserResponse)
async def create_user(user_create: UserCreate, db:Session = Depends(get_db)): # <-- Usa UserCreate
    db_user = db.query(User).filter(User.email == user_create.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    
    hashed_password = get_password_hash(user_create.password)
    
    new_user = User(
        nombre=user_create.nombre,
        email=user_create.email,
        hashed_password=hashed_password,
        fecha_registro=datetime.now(), # Generamos la fecha aquí
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user.get("/users/me", response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    # La dependencia nos da el objeto User de la BD
    # El response_model=UserResponse se encarga de convertirlo al formato seguro
    return current_user

@user.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Los endpoints de PUT y DELETE se pueden ajustar de forma similar si es necesario.

# --- AÑADE ESTE NUEVO ENDPOINT ---
@user.put("/users/me/language", response_model=UserResponse)
def select_user_language(
    request: SelectLanguageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el idioma de aprendizaje actual del usuario autenticado.
    """
    # Verificamos si el idioma que se quiere asignar existe
    idioma_a_asignar = db.query(Idioma).filter(Idioma.id == request.id_idioma).first()
    if not idioma_a_asignar:
        raise HTTPException(status_code=404, detail="El idioma seleccionado no existe.")
        
    current_user.id_idioma_actual = request.id_idioma
    db.commit()
    db.refresh(current_user)
    return current_user