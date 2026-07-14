from abc import ABC, abstractmethod
from rpg_tasks.core.domain.entidades import Usuario
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]: 
        pass

    @abstractmethod
    def nombre_usuario_existe(self, nombre_usuario: str): 
        pass

    @abstractmethod
    def registrar_usuario(self, usuario: Usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str, token_usuario: str, id_externo_usuario_en_plataforma: str):
        pass

    @abstractmethod
    def autenticar_usuario(self, nombre_usuario:str, password_usuario:str):
        pass
