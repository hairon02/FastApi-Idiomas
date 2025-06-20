# En schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- Esquema Base ---
# Contiene los campos comunes que no son sensibles y no tienen validaciones estrictas de entrada.
class UserBase(BaseModel):
    nombre: str
    email: EmailStr

# --- Esquema para la Creación de un Usuario (Datos de ENTRADA) ---
# Hereda de UserBase y añade el campo de la contraseña para el registro.
class UserCreate(UserBase):
    # El frontend enviará un campo "password".
    password: str = Field(..., min_length=6)

# --- Esquema para la Respuesta al Cliente (Datos de SALIDA) ---
# Define exactamente qué campos queremos devolver. ¡Nunca la contraseña!
class UserResponse(UserBase):
    id: int
    fecha_registro: datetime
    # En el futuro aquí podríamos añadir id_idioma_actual, etc.
    id_idioma_actual: Optional[int] = None
    model_config = ConfigDict(
        from_attributes=True  # Permite que se cree desde un objeto de base de datos
    )

class SelectLanguageRequest(BaseModel):
    id_idioma: int