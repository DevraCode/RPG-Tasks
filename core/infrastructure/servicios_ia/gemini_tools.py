from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from core.application.use_cases.ia.usuarios_ia_use_cases  import UsuarioIAUsecase
from core.application.use_cases.ia.personajes_ia_use_cases import PersonajesIAUsecase

from core.infrastructure.dbconfig import db_config



def gemini_tools(db_config):

    repo_usuarios = MySQLUsuarioRepository(db_config)
    usuarios = UsuarioIAUsecase(repo_usuarios)
    repo_personajes = MySQLPersonajesRepository(db_config)
    personajes = PersonajesIAUsecase(repo_usuarios,repo_personajes)


    busca_usuario_ia = usuarios.buscar_usuario_ia
    descripcion_personaje = personajes.descripcion_personaje


    return [
        busca_usuario_ia,
        descripcion_personaje
    ]

