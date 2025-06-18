from fastapi import FastAPI
from routers.user import user
from routers.auth import auth
from routers.idioma import idioma
from middleware.cors import setup_cors
from routers.leccion import leccion
from routers.nivel import nivel
from routers.actividad import actividad

app = FastAPI()

setup_cors(app)

app.include_router(user, tags=["users"])
app.include_router(auth, tags=["auth"])
app.include_router(idioma, tags=["idiomas"])
app.include_router(leccion, tags=["lecciones"])
app.include_router(nivel, tags=["niveles"])
app.include_router(actividad, tags=["actividades"])

@app.get("/")
def read_root():
    return {"mensaje": "Servidor FastAPI en ejecucion"}


