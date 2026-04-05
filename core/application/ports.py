# core/application/ports.py
from abc import ABC, abstractmethod
from core.domain.models import Usuario, Personaje
from typing import Optional

class UsuarioRepository(ABC):
    @abstractmethod
    def buscar_por_id_externo(self, id_ext: str, plataforma: str) -> Optional[Usuario]:
        """Busca si un ID de Telegram/Discord ya tiene una cuenta maestra."""
        pass

    @abstractmethod
    def registrar_usuario_completo(self, usuario: Usuario, plataforma: str, id_ext: str, personaje: Personaje):
        """Guarda todo: Usuario, su Vinculación y su Personaje inicial."""
        pass