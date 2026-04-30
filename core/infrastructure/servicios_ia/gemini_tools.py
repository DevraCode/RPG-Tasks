from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases.ia.usuarios_ia_use_cases  import UsuarioIAUsecase

from core.infrastructure.dbconfig import db_config



def gemini_tools(db_config):

    repo_usuarios = MySQLUsuarioRepository(db_config)
    usuarios = UsuarioIAUsecase(repo_usuarios)


    busca_usuario_ia = usuarios.buscar_usuario_ia
    return [
        busca_usuario_ia
    ]