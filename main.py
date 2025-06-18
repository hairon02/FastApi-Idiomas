from fastapi import FastAPI
from routers.user import user
from routers.auth import auth
from routers.idioma import idioma
from middleware.cors import setup_cors
from routers.leccion import leccion
from routers.nivel import nivel
from routers.actividad import actividad
from routers.actividad_oracion import actividad_oracion
from routers.actividad_video import actividad_video
from routers.actividad_vocabulario import actividad_vocabulario
from routers.actividad_voz import actividad_voz
from routers.progreso import progreso_router

app = FastAPI()

setup_cors(app)

app.include_router(user, tags=["users"])
app.include_router(auth, tags=["auth"])
app.include_router(idioma, tags=["idiomas"])
app.include_router(leccion, tags=["lecciones"])
app.include_router(nivel, tags=["niveles"])
app.include_router(actividad, tags=["actividades"])
app.include_router(actividad_oracion, tags=["actividad_oracion"]) 
app.include_router(actividad_video, tags=["actividad_video"])   
app.include_router(actividad_vocabulario, tags=["actividad_vocabulario"])
app.include_router(actividad_voz, tags=["actividad_voz"])
app.include_router(progreso_router, tags=["progreso"])

@app.get("/")
def read_root():
    return {"mensaje": "Servidor FastAPI en ejecucion"}


