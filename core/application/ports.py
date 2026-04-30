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
    def buscar_usuario_por_nombre(self,nombre_usuario:str): #Busca al usuario por el nombre
        pass

    @abstractmethod
    def buscar_usuario_por_plataforma(self, plataforma:str): #Busca al usuario por plataforma
        pass

    @abstractmethod
    def buscar_usuario_en_bd (self, nombre_usuario: str): #Busca al usuario por nombre en la db
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

    
  
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

class TareasRepository(ABC):
    @abstractmethod
    def insertar_tarea(self, id_usuario, nombre_tarea):
        pass


