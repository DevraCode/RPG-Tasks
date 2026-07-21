from abc import ABC, abstractmethod

class OllamaOutputPort(ABC):
    @abstractmethod
    def generar_descripcion(self, prompt: str) -> str:
        pass