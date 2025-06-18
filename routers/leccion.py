from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.leccion import LeccionCreate, LeccionResponse
from models.leccion import Leccion
from models.actividad import Actividad
from schemas.enums import TipoActividadEnum
from models.actividad_vocabulario import ActividadVocabulario
from models.actividad_oracion import ActividadOracion
from models.actividad_video import ActividadVideo
from models.actividad_voz import ActividadVoz
from routers.auth import get_current_user

leccion = APIRouter(dependencies=[Depends(get_current_user)])

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

@leccion.get('/lecciones/{id_leccion}/actividades', response_model=list[LeccionResponse])
async def get_actividades_por_leccion(id_leccion: int, db: Session = Depends(get_db)):
    leccion = db.query(Leccion).filter(Leccion.id == id_leccion).first()
    if not leccion:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    actividades = db.query(Leccion).filter(Leccion.id == id_leccion).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No se encontraron actividades para esta lección")
    
    return actividades

@leccion.get("/lecciones/actividades/{id_leccion}")
def get_actividades(id_leccion: int, db: Session = Depends(get_db)):
    # ✅ Buscar las actividades de la lección
    actividades = db.query(Actividad).filter(Actividad.id_leccion == id_leccion).order_by(Actividad.orden).all()

    if not actividades:
        raise HTTPException(status_code=404, detail="No se encontraron actividades para esta lección.")

    resultado = []

    for actividad in actividades:
        contenido = {}

        if actividad.tipo_actividad == TipoActividadEnum.VOCABULARIO:
            detalle = db.query(ActividadVocabulario).filter(ActividadVocabulario.id_actividad == actividad.id).first()
            if detalle:
                contenido = {
                    "palabra": detalle.palabra,
                    "traduccion": detalle.traduccion,
                    "url_audio": detalle.url_audio
                }

        elif actividad.tipo_actividad == TipoActividadEnum.ORACION:
            detalle = db.query(ActividadOracion).filter(ActividadOracion.id_actividad == actividad.id).first()
            if detalle:
                contenido = {
                    "frase_correcta": detalle.frase_correcta,
                    "banco_palabras": detalle.banco_palabras
                }

        elif actividad.tipo_actividad == TipoActividadEnum.VIDEO:
            detalle = db.query(ActividadVideo).filter(ActividadVideo.id_actividad == actividad.id).first()
            if detalle:
                contenido = {
                    "id_video_youtube": detalle.id_video_youtube,
                    "palabra_clave": detalle.palabra_clave
                }

        elif actividad.tipo_actividad == TipoActividadEnum.VOZ:
            detalle = db.query(ActividadVoz).filter(ActividadVoz.id_actividad == actividad.id).first()
            if detalle:
                contenido = {
                    "frase_a_repetir": detalle.frase_a_repetir
                }

        resultado.append({
            "orden": actividad.orden,
            "tipo": actividad.tipo_actividad,  # Usa el nombre correcto del campo
            "contenido": contenido
        })

    return resultado

