from deep_translator import GoogleTranslator as RealTimeGoogle

from core.infrastructure.repositorios.mysql_usuario_repository import UsuarioRepository
from core.application.use_cases.basico import usuarios_use_cases
from core.infrastructure.dbconfig import db_config

from contextvars import ContextVar

#Diccionario para guardar el idioma del usuario
IDIOMAS_USUARIOS = {}

repo_usuario = UsuarioRepository(db_config)
usuario = usuarios_use_cases(repo_usuario)


idioma_contexto = ContextVar("idioma_usuario_actual", default="es")

#Funcion que se conecta a GoogleTranslator y traduce el texto que se le pasa como parámetro
def traducir(texto: str, lang: str) -> str:
        if lang.startswith('es'):
            return texto
            
        try:
            return RealTimeGoogle(source='es', target=lang).translate(texto)
        
        except Exception as e:
            print(f"Error en la API de traducción: {e}")
            return texto 
        

def traduccion(texto):
    idioma_actual = idioma_contexto.get()
    return traducir(texto=texto, lang=idioma_actual)

