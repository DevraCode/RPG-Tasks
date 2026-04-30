from abc import ABC, abstractmethod
from core.domain.models import Usuario
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_por_id_usuario(self, id_usuario: int) -> Optional[Usuario]: 
        pass

    @abstractmethod
    def buscar_por_id_externo(self, id_ext: str) -> Optional[Usuario]: 
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
    def comprobar_usuario_contraseña(self, nombre_usuario:str, password_usuario:str):
        pass

    @abstractmethod
    def buscar_usuario_ia(self, nombre_usuario:str):
        pass