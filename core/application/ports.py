# core/application/ports.py
from abc import ABC, abstractmethod
from core.domain.models import Usuario, Personaje
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_por_id_externo(self, id_ext: str, plataforma: str) -> Optional[Usuario]:
        
        pass

    @abstractmethod
    def buscar_usuario_por_nombre(self,id_usuario:str): #Busca al usuario por el nombre
        pass

    @abstractmethod
    def buscar_usuario_por_plataforma(self, plataforma:str): #Busca al usuario por plataforma
        pass

    @abstractmethod
    def buscar_usuario_en_bd (self, nombre_usuario: str): #Busca al usuario por nombre en la db
        pass
    
    @abstractmethod
    def registrar_usuario_completo(self, usuario: Usuario, plataforma: str, id_ext: str, personaje: Personaje):
        
        pass

