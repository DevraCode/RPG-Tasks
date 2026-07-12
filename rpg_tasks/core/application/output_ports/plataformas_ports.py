from abc import ABC, abstractmethod



class PlataformasRepository(ABC):
    @abstractmethod
    def token_existe(self, token_usuario: str):
        pass
    
    @abstractmethod
    def vincular_plataforma(self, id_usuario: int):
        pass 
