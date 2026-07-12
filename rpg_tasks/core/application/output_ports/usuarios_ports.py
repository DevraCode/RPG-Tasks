from abc import ABC, abstractmethod
from rpg_tasks.core.domain.entidades import Usuario
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]: 
        pass

    @abstractmethod
    def buscar_por_id_externo(self, id_ext: str) -> Optional[Usuario]: 
        pass

    @abstractmethod
    def nombre_usuario_existe(self, nombre_usuario: str): 
        pass

    @abstractmethod
    def buscar_usuario_por_nombre(self,nombre_usuario:str): 
        pass

    @abstractmethod
    def buscar_usuario_por_plataforma(self, plataforma:str): 
        pass

    @abstractmethod
    def buscar_usuario_en_bd (self, nombre_usuario: str): 
        pass

    @abstractmethod
    def registrar_usuario(self, usuario: Usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        pass

    @abstractmethod
    def autenticar_usuario(self, nombre_usuario:str, password_usuario:str):
        pass
