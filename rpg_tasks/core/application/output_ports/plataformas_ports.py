from abc import ABC, abstractmethod



class PlataformasRepository(ABC):

    @abstractmethod
    def id_externo_usuario_existe(self, id_externo_usuario: str):
        pass

    @abstractmethod
    def id_usuario_en_plataforma_existe(self, id_externo_usuario_en_plataforma):
        pass

    @abstractmethod
    def token_existe(self, token_usuario: str):
        pass
    
    @abstractmethod
    def vincular_plataforma(self, id_usuario: int, id_externo_usuario:str, token_usuario:str, id_externo_usuario_en_plataforma:str,):
        pass

    @abstractmethod
    def cerrar_sesion(self, token_usuario: str):
        pass
