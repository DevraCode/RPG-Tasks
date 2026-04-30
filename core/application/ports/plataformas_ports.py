from abc import ABC, abstractmethod
from core.domain.models import Usuario
from typing import Optional


class PlataformasRepository(ABC):
    @abstractmethod
    def vincular_id_externo_con_interno(self, id_externo_usuario: str):
        pass
    
    @abstractmethod
    def vincular_plataforma(self, id_usuario: int):
        pass 

    @abstractmethod
    def obtener_estado_sesion(self, id_externo_usuario: str):
        pass

    @abstractmethod
    def iniciar_sesion(self, id_usuario: int):
        pass

    @abstractmethod
    def cerrar_sesion(self, id_usuario: int):
        pass

    @abstractmethod
    def sesion_cerrada(self, id_externo_usuario: str):
        pass