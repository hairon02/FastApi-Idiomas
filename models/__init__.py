
# Importa la base declarativa
from db.database import Base

# Importa todas tus clases de modelos de los archivos individuales
# Esto asegura que todas las clases se carguen y se registren con Base.metadata

from .idioma import Idioma
from .nivel import Nivel
from .leccion import Leccion
from .actividad import Actividad
from .actividad_vocabulario import ActividadVocabulario
from .actividad_oracion import ActividadOracion
from .actividad_video import ActividadVideo
from .actividad_voz import ActividadVoz
from .user import User
from .progreso_leccion import ProgresoLeccion 
from .progreso_vocabulario import ProgresoVocabulario