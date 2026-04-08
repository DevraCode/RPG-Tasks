from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: str
    nombre_usuario: str
    password_usuario: str
    activo: bool = True

@dataclass
class Personaje:
    id_usuario: str
    clase: str = "Aprendiz"
    nivel: int = 1
    exp: int = 0
    oro: int = 0