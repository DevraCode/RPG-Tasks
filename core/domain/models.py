from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

class CorrespondenciaPlataformas(IntEnum):
    WEB = 1
    ANDROID = 2
    TELEGRAM = 3
    DISCORD = 4


@dataclass
class Usuario:
    id_usuario: str
    id_externo_usuario: str = "0"
    nombre_usuario: str = None
    password_usuario: str = None
    email_usuario : str = None
    fecha_registro: datetime = None
    activo: bool = True

@dataclass
class Personaje:
    id_usuario: str
    id_personaje: int = 00
    nombre_personaje: str = "Personaje"
    genero: str = "Masculino"
    clase: str = "Aprendiz"
    nivel: int = 1
    exp: int = 0
    evolucion: int = 0
    icono_personaje: str = "Ruta_Imagen"
    imagen_personaje: str = "Ruta_Imagen"
    animacion_personaje : str = "Ruta_imagen"

@dataclass
class Plataformas:
    id_plataforma: int
    nombre_plataforma: str
