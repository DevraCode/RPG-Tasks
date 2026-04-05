from dataclasses import dataclass

@dataclass
class Usuario:
    id_interno: str
    nombre_jugador: str
    activo: bool = True

@dataclass
class Personaje:
    id_interno: str
    clase: str
    nivel: int = 1
    exp: int = 0
    oro: int = 0