from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: str
    nombre_usuario: str
    id_externo_usuario: str = "0"
    password_usuario: str = None
    plataforma: str = None
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
    avatar_personaje: str = "Ruta_Imagen"
    imagen_personaje: str = "Ruta_Imagen"
    imagen_personaje_ataque: str = "Ruta_Imagen"
    imagen_personaje_defensa: str = "Ruta_Imagen"
