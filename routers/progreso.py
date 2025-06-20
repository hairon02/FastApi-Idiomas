from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.nivel import Nivel
from models.progreso_leccion import ProgresoLeccion
from models.progreso_vocabulario import ProgresoVocabulario
from schemas.enums import EstadoLeccionEnum, EstadoVocabEnum
from schemas.user import UserResponse  # Asegúrate de que esta importación esté
from datetime import datetime
from pydantic import BaseModel
from routers.auth import get_current_user
from models.leccion import Leccion

# Quitamos la dependencia de aquí
progreso_router = APIRouter(tags=["progreso"])


@progreso_router.get("/progreso/estado-actual")
def obtener_estado_actual(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if current_user.id_idioma_actual is None:
        return {
            "leccion_actual": None,
            "vocabulario_aprendido": [],
            "progreso_lecciones": {}
        }

    progreso_lecciones_db = db.query(ProgresoLeccion).filter(
        ProgresoLeccion.id_usuario == current_user.id
    ).all()

    progreso_lecciones_map = {
        progreso.id_leccion: progreso.estado.value 
        for progreso in progreso_lecciones_db
    }

    leccion_actual = None
    progreso_actual_obj = None
    lecciones_del_idioma = db.query(Leccion).join(Nivel).filter(Nivel.id_idioma == current_user.id_idioma_actual).order_by(Leccion.id).all()

    for leccion in lecciones_del_idioma:
        estado = progreso_lecciones_map.get(leccion.id)
        if estado != 'COMPLETADA':
            leccion_actual = leccion
            progreso_actual_obj = next((p for p in progreso_lecciones_db if p.id_leccion == leccion.id), None)
            break
            
    # --- AQUÍ ESTÁ LA CORRECCIÓN ---
    # Reemplazamos el .filter(...) por el filtro correcto
    vocabulario = db.query(ProgresoVocabulario).filter(
        ProgresoVocabulario.id_usuario == current_user.id
    ).all()
    # --- FIN DE LA CORRECCIÓN ---

    vocabulario_aprendido = [{"id_palabra": p.id_palabra, "estado_aprendizaje": p.estado_aprendizaje.value, "aciertos": p.aciertos, "fallos": p.fallos} for p in vocabulario]

    return {
        "leccion_actual": {
            "id": leccion_actual.id,
            "titulo": leccion_actual.titulo,
            "estado": progreso_actual_obj.estado.value if progreso_actual_obj else 'NO_INICIADA',
            "ultima_actividad": progreso_actual_obj.ultima_actividad if progreso_actual_obj else 0
        } if leccion_actual else None,
        "vocabulario_aprendido": vocabulario_aprendido,
        "progreso_lecciones": progreso_lecciones_map
    }


class ActualizarProgresoLeccionRequest(BaseModel):
    estado: EstadoLeccionEnum
    ultima_actividad: int

@progreso_router.post("/progreso/lecciones/{id_leccion}")
# Añadimos la dependencia directamente aquí
def actualizar_progreso_leccion(id_leccion: int, datos: ActualizarProgresoLeccionRequest, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    progreso = db.query(ProgresoLeccion).filter_by(id_usuario=current_user.id, id_leccion=id_leccion).first()

    if not progreso:
        progreso = ProgresoLeccion(
            id_usuario=current_user.id,
            id_leccion=id_leccion,
            estado=datos.estado,
            ultima_actividad=datos.ultima_actividad,
            fecha_ultimo_acceso=datetime.utcnow()
        )
        db.add(progreso)
    else:
        progreso.estado = datos.estado
        progreso.ultima_actividad = datos.ultima_actividad
        progreso.fecha_ultimo_acceso = datetime.now()

    db.commit()
    db.refresh(progreso)
    return {"mensaje": "Progreso de la lección actualizado correctamente."}


class ActualizarProgresoVocabRequest(BaseModel):
    id_palabra: int
    aciertos: int = 0
    fallos: int = 0
    estado_aprendizaje: EstadoVocabEnum

@progreso_router.post("/progreso/vocabulario")
# Añadimos la dependencia directamente aquí
def actualizar_progreso_vocabulario(datos: ActualizarProgresoVocabRequest, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    progreso = db.query(ProgresoVocabulario).filter_by(id_usuario=current_user.id, id_palabra=datos.id_palabra).first()

    if not progreso:
        progreso = ProgresoVocabulario(
            id_usuario=current_user.id,
            id_palabra=datos.id_palabra,
            estado_aprendizaje=datos.estado_aprendizaje,
            aciertos=datos.aciertos,
            fallos=datos.fallos,
            fecha_ultimo_repaso=datetime.now()
        )
        db.add(progreso)
    else:
        progreso.aciertos = datos.aciertos
        progreso.fallos = datos.fallos
        progreso.estado_aprendizaje = datos.estado_aprendizaje
        progreso.fecha_ultimo_repaso = datetime.now()

    db.commit()
    db.refresh(progreso)
    return {"mensaje": "Progreso de vocabulario actualizado correctamente."}