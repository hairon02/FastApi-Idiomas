from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.progreso_leccion import ProgresoLeccion
from models.progreso_vocabulario import ProgresoVocabulario
from schemas.enums import EstadoLeccionEnum, EstadoVocabEnum
from schemas.user import UserResponse  # Asegúrate de que esta importación esté
from datetime import datetime
from pydantic import BaseModel
from routers.auth import get_current_user

# Quitamos la dependencia de aquí
progreso_router = APIRouter(tags=["progreso"])


@progreso_router.get("/progreso/estado-actual")
# Añadimos la dependencia directamente aquí
def obtener_estado_actual(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    # Buscamos el progreso usando el ID del usuario que nos da la dependencia
    progreso_lecciones = db.query(ProgresoLeccion).filter(
        ProgresoLeccion.id_usuario == current_user.id
    ).order_by(ProgresoLeccion.id_leccion).all()

    leccion_actual = None
    progreso_actual = None
    for progreso in progreso_lecciones:
        if progreso.estado != EstadoLeccionEnum.COMPLETADA:
            leccion_actual = progreso.leccion
            progreso_actual = progreso
            break

    vocabulario = db.query(ProgresoVocabulario).filter(
        ProgresoVocabulario.id_usuario == current_user.id
    ).all()

    vocabulario_aprendido = []
    for palabra in vocabulario:
        vocabulario_aprendido.append({
            "id_palabra": palabra.id_palabra,
            "estado_aprendizaje": palabra.estado_aprendizaje,
            "aciertos": palabra.aciertos,
            "fallos": palabra.fallos
        })

    return {
        "leccion_actual": {
            "id": leccion_actual.id if leccion_actual else None,
            "titulo": leccion_actual.titulo if leccion_actual else None,
            "estado": progreso_actual.estado if progreso_actual else None,
            "ultima_actividad": progreso_actual.ultima_actividad if progreso_actual else None
        } if leccion_actual else None,
        "vocabulario_aprendido": vocabulario_aprendido
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