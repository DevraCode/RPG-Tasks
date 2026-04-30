from abc import ABC, abstractmethod
from core.domain.models import Usuario
from typing import Optional

class TareasRepository(ABC):
    @abstractmethod
    def insertar_tarea(self, id_usuario, nombre_tarea):
        pass


