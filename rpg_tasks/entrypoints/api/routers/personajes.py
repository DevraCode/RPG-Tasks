
#IMPORTACIONES
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
#-----------------------------------------------------------------------------------------------------------------------------
from rpg_tasks.infrastructure.dbconfig import db_config
from rpg_tasks.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from rpg_tasks.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from rpg_tasks.core.application.use_cases.personajes_use_cases import PersonajeUseCase

from rpg_tasks.infrastructure.servicios_ia.adaptador_ollama import OllamaAdapter
from rpg_tasks.infrastructure.servicios_ia.config_ia import SYSTEM_INSTRUCTION

adaptador_ollama = OllamaAdapter(system_instructions=SYSTEM_INSTRUCTION)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INICIALIZACIÓN DE REPOSITORIOS Y CASOS DE USO
repo_usuario = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)
personajes_use_case = PersonajeUseCase(repo_usuario, repo_personajes, adaptador_ollama)



#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Router de FastAPI para los endpoints relacionados con personajes
router = APIRouter(
    prefix="/api/personajes",
    tags=["Personajes"])

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#DTOs
class RegistrarPersonajeDTO(BaseModel):
    nombre_personaje: str
    genero: str
    clase: str
    imagen_personaje: str
    icono_personaje: str
    animacion_personaje: str
    descripcion_personaje: str

#ENDPOINTS
#Catálogo de personajes
@router.get("")
def mostrar_personajes():
    return personajes_use_case.personajes_dic()

