from abc import ABC, abstractmethod



class PlataformasRepository(ABC):

    @abstractmethod
    def id_externo_usuario_existe(self, id_externo_usuario: str):
        pass

    @abstractmethod
    def token_existe(self, token_usuario: str):
        pass
    
    @abstractmethod
    def vincular_plataforma(self, id_usuario: int):
        pass 
