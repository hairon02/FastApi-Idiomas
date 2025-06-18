from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from models.user import User
from db.database import get_db
from routers.auth import get_password_hash
user = APIRouter()


@user.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@user.post("/users", response_model=UserResponse)
async def create_user(user_create: UserCreate, db:Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == user_create.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    new_user = User(
        nombre = user_create.nombre,
        email = user_create.email,
        hashed_password = get_password_hash(user_create.hashed_password), # Hash the password before saving
        fecha_registro = user_create.fecha_registro  # Use current time if not provided
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.nombre = user_update.nombre
    user.email = user_update.email
    user.hashed_password = get_password_hash(user_update.hashed_password)
    db.commit()
    db.refresh(user)
    return user

@user.delete("/users/delete/{id}", response_model = UserResponse)
def delete(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Verificar si el usuario a actualizar existe
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_user)
    db.commit()
    return { "detail": "User deleted successfully" }