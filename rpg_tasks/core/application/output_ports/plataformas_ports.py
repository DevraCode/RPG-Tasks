from abc import ABC, abstractmethod



class PlataformasRepository(ABC):
    @abstractmethod
    def id_externo_existe(self, id_usuario: str):
        pass
    
    @abstractmethod
    def vincular_plataforma(self, id_usuario: int):
        pass 
