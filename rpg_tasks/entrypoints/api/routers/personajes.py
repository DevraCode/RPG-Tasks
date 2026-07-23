
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
personajes_use_case = PersonajeUseCase(repo_personajes, repo_usuario, adaptador_ollama)



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
    id_usuario_en_plataforma: str

#ENDPOINTS
#Catálogo de personajes
@router.get("")
def mostrar_personajes():
    return personajes_use_case.personajes_dic()

@router.post("/seleccionar", status_code=status.HTTP_201_CREATED)
def seleccionar_personaje(datos:RegistrarPersonajeDTO):
    
    try:
        #El caso de uso registra al personaje y devuelve la descripcion.
        #Podría devolver el objeto entero, pero me resulta más cómodo así :)
        registro_personaje_y_devuelve_descripcion = personajes_use_case.registrar_personaje(
            nombre_personaje=datos.nombre_personaje,
            genero=datos.genero,
            clase=datos.clase,
            imagen_personaje=datos.imagen_personaje,
            icono_personaje=datos.icono_personaje,
            animacion_personaje=datos.animacion_personaje,
            descripcion_personaje=datos.descripcion_personaje,
            id_usuario_en_plataforma=datos.id_usuario_en_plataforma)
    
        return {
                "status": "success",
            "nombre_personaje": datos.nombre_personaje,
            "clase": datos.clase,
            "imagen_personaje": datos.imagen_personaje,
            "descripcion_personaje": registro_personaje_y_devuelve_descripcion
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar: {str(e)}")

