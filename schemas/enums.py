from enum import Enum

# Enum para los tipos de actividad
class TipoActividadEnum(str, Enum):
    """
    Define los tipos de actividades disponibles en la aplicación.
    Corresponde al ENUM 'tipo_actividad_enum' en PostgreSQL.
    """
    VOCABULARIO = "VOCABULARIO"
    ORACION = "ORACION"
    VIDEO = "VIDEO"
    VOZ = "VOZ"

# Enum para el estado de una lección
class EstadoLeccionEnum(str, Enum):
    """
    Define los posibles estados de una lección para el progreso del usuario.
    Corresponde al ENUM 'estado_leccion_enum' en PostgreSQL.
    """
    NO_INICIADA = "NO_INICIADA"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"

# Enum para el estado de aprendizaje del vocabulario
class EstadoVocabEnum(str, Enum):
    """
    Define los estados de aprendizaje de una palabra de vocabulario.
    Corresponde al ENUM 'estado_vocab_enum' en PostgreSQL.
    """
    NUEVA = "NUEVA"
    APRENDIENDO = "APRENDIENDO"
    DOMINADA = "DOMINADA"
