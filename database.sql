-- Crear tipos de datos personalizados (ENUMs) para mejor consistencia
CREATE TYPE tipo_actividad_enum AS ENUM ('VOCABULARIO', 'ORACION', 'VIDEO', 'VOZ');
CREATE TYPE estado_leccion_enum AS ENUM ('NO_INICIADA', 'EN_PROGRESO', 'COMPLETADA');
CREATE TYPE estado_vocab_enum AS ENUM ('NUEVA', 'APRENDIENDO', 'DOMINADA');


-- TABLAS DE CONTENIDO --

-- Tabla para almacenar los idiomas disponibles en la aplicación
CREATE TABLE Idiomas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    codigo_iso VARCHAR(10) UNIQUE,
    url_bandera VARCHAR(255)
);

-- Tabla para los niveles de cada idioma
CREATE TABLE Niveles (
    id SERIAL PRIMARY KEY,
    id_idioma INTEGER NOT NULL REFERENCES Idiomas(id) ON DELETE CASCADE,
    numero_nivel INTEGER NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    UNIQUE (id_idioma, numero_nivel)
);

-- Tabla para las lecciones dentro de cada nivel
CREATE TABLE Lecciones (
    id SERIAL PRIMARY KEY,
    id_nivel INTEGER NOT NULL REFERENCES Niveles(id) ON DELETE CASCADE,
    numero_leccion INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    UNIQUE (id_nivel, numero_leccion)
);

-- Tabla maestra que define el orden y tipo de cada actividad en una lección
CREATE TABLE Actividades (
    id SERIAL PRIMARY KEY,
    id_leccion INTEGER NOT NULL REFERENCES Lecciones(id) ON DELETE CASCADE,
    orden INTEGER NOT NULL,
    tipo_actividad tipo_actividad_enum NOT NULL,
    UNIQUE (id_leccion, orden)
);

-- Tablas "satélite" con el contenido específico de cada tipo de actividad
CREATE TABLE Actividad_Vocabulario (
    id SERIAL PRIMARY KEY,
    id_actividad INTEGER NOT NULL UNIQUE REFERENCES Actividades(id) ON DELETE CASCADE,
    palabra VARCHAR(100) NOT NULL,
    traduccion VARCHAR(100) NOT NULL,
    url_audio VARCHAR(255)
);

CREATE TABLE Actividad_Oraciones (
    id SERIAL PRIMARY KEY,
    id_actividad INTEGER NOT NULL UNIQUE REFERENCES Actividades(id) ON DELETE CASCADE,
    frase_correcta TEXT NOT NULL,
    banco_palabras JSONB NOT NULL
);

CREATE TABLE Actividad_Video (
    id SERIAL PRIMARY KEY,
    id_actividad INTEGER NOT NULL UNIQUE REFERENCES Actividades(id) ON DELETE CASCADE,
    id_video_youtube VARCHAR(50) NOT NULL,
    palabra_clave VARCHAR(100)
    url_video_cloudinary TEXT
);

CREATE TABLE Actividad_Voz (
    id SERIAL PRIMARY KEY,
    id_actividad INTEGER NOT NULL UNIQUE REFERENCES Actividades(id) ON DELETE CASCADE,
    frase_a_repetir TEXT NOT NULL
);


-- TABLAS DE USUARIO Y PROGRESO --

-- Tabla para almacenar los datos de los usuarios
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de unión para rastrear el progreso de los usuarios en las lecciones
CREATE TABLE Progreso_Lecciones (
    id_usuario INTEGER NOT NULL REFERENCES Usuarios(id) ON DELETE CASCADE,
    id_leccion INTEGER NOT NULL REFERENCES Lecciones(id) ON DELETE CASCADE,
    estado estado_leccion_enum NOT NULL DEFAULT 'NO_INICIADA',
    ultima_actividad INTEGER NOT NULL DEFAULT 0,
    fecha_ultimo_acceso TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    puntuacion_alta INTEGER DEFAULT 0,
    PRIMARY KEY (id_usuario, id_leccion)
);

-- Tabla de unión para rastrear el progreso de los usuarios con cada palabra del vocabulario
CREATE TABLE Progreso_Vocabulario (
    id_usuario INTEGER NOT NULL REFERENCES Usuarios(id) ON DELETE CASCADE,
    id_palabra INTEGER NOT NULL REFERENCES Actividad_Vocabulario(id) ON DELETE CASCADE,
    estado_aprendizaje estado_vocab_enum NOT NULL DEFAULT 'NUEVA',
    aciertos INTEGER NOT NULL DEFAULT 0,
    fallos INTEGER NOT NULL DEFAULT 0,
    fecha_ultimo_repaso TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id_usuario, id_palabra)
);