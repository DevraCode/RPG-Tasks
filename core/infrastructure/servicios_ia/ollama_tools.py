from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from core.application.use_cases.ia.usuarios_ia_use_cases import UsuarioIAUsecase
from core.application.use_cases.ia.personajes_ia_use_cases import PersonajesIAUsecase
from core.infrastructure.dbconfig import db_config
import inspect

#Función auxiliar que traduce las funciones para las tools de ollama
def traducir_para_ollama(func):
    
    #Identifica los parámetros de la función a traducir que no sean 'self'
    sig = inspect.signature(func)
    params = {
        name: {"type": "string"} 
        for name in sig.parameters if name != 'self'
    }
    
    #Devuelve el diccionario que necesita ollama en lugar del objeto proporcionado por la función
    return {
        'type': 'function',
        'function': {
            'name': func.__name__,
            'description': func.__doc__ or "Sin descripción",
            'parameters': {
                'type': 'object',
                'properties': params,
                'required': list(params.keys())
            }
        }
    }

class OllamaTools:
    def __init__(self):
        self.repo_usuarios = MySQLUsuarioRepository(db_config)
        self.repo_personajes = MySQLPersonajesRepository(db_config)
        self.usuarios = UsuarioIAUsecase(self.repo_usuarios)
        self.personajes = PersonajesIAUsecase(self.repo_personajes,self.repo_personajes)


    def ollama_tools(self):
        busca_usuario_ia = traducir_para_ollama(self.usuarios.buscar_usuario_ia)
        descripcion_personaje = traducir_para_ollama(self.personajes.descripcion_personaje)


        return [
            busca_usuario_ia,
            descripcion_personaje
        ]

