from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository

from core.application.use_cases.ia.usuarios_ia_use_cases import UsuarioIAUsecase
from core.application.use_cases.ia.personajes_ia_use_cases import PersonajesIAUsecase

from core.infrastructure.dbconfig import db_config


class OllamaTools:
    def __init__(self):
        self.repo_usuarios = MySQLUsuarioRepository(db_config)
        self.repo_personajes = MySQLPersonajesRepository(db_config)
        self.usuarios = UsuarioIAUsecase(self.repo_usuarios)
        self.personajes = PersonajesIAUsecase(self.repo_personajes,self.repo_personajes)


    def ollama_tools(self):
        busca_usuario_ia = self.usuarios.buscar_usuario_ia
        descripcion_personaje = self.personajes.descripcion_personaje


        return [
            busca_usuario_ia,
            descripcion_personaje
        ]

