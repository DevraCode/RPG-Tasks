from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: str
    nombre_usuario: str
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