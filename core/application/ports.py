
from abc import ABC, abstractmethod
from core.domain.models import Usuario, Personaje
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_por_id_usuario(self, id_usuario: str) -> Optional[Usuario]: 
        pass

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
    def limite_personajes_de_usuario(self, id_usuario: str): #Busca al usuario por nombre en la db
        pass

    @abstractmethod
    def registrar_personaje_elegido(self, id_usuario: str, nombre_personaje: str, genero: str, clase: str, imagen_personaje: str, icono_personaje: str, animacion_personaje:str):
        pass

    @abstractmethod
    def iniciar_sesion(self, id_externo_usuario: str):
        pass
    
    @abstractmethod
    def obtener_estado_sesion(self, id_externo_usuario: str, nombre_plataforma: str):
        pass

    @abstractmethod
    def cerrar_sesion(self, id_externo_usuario: str):
        pass

    @abstractmethod
    def sesion_cerrada(self, id_externo_usuario: str):
        pass

    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #TELEGRAM / DISCORD
    @abstractmethod
    def registrar_usuario_telegram_discord(self, usuario: Usuario, plataforma: str, id_ext: str):
        pass

    def vincular_id_personaje_con_usuario(self, id_usuario:str):
        pass
    
    #Esto para Telegram / Discord    
    @abstractmethod
    def vincular_id_externo_con_interno(self, id_externo_usuario: str):
        pass

