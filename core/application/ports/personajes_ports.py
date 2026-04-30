from abc import ABC, abstractmethod
from core.domain.models import Usuario
from typing import Optional

class PersonajesRepository(ABC):
    @abstractmethod
    def registrar_personaje_elegido(self, id_usuario: str, nombre_personaje: str, genero: str, clase: str, imagen_personaje: str, icono_personaje: str, animacion_personaje:str):
        pass

    @abstractmethod
    def limite_personajes_de_usuario(self, id_usuario: str): 
        pass

    @abstractmethod
    def lista_personajes_usuario(id_usuario:str):
        pass

    @abstractmethod
    def vincular_id_personaje_con_usuario(self, id_usuario:int):
        pass

