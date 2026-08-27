#IMPORTACIONES
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
#-----------------------------------------------------------------------------------------------------------------------------
from rpg_tasks.infrastructure.dbconfig import db_config
from rpg_tasks.infrastructure.repositorios.mysql_plataformas_repository import MySQLPlataformasRepository
from rpg_tasks.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from rpg_tasks.core.application.use_cases.plataformas_use_cases import PlataformasUseCase


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INICIALIZACIÓN DE REPOSITORIOS Y CASOS DE USO
repo_plataformas = MySQLPlataformasRepository(db_config)
repo_usuarios = MySQLUsuarioRepository(db_config)
plataformas_use_case = PlataformasUseCase(repo_plataformas, repo_usuarios)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Router de FastAPI para los endpoints relacionados con usuarios
router = APIRouter(
    prefix="/api/plataformas",
    tags=["Plataformas"])

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#DTOs

#DTO para la vinculación de usuarios
class VincularUsuarioDTO(BaseModel):
    nombre_usuario: str
    password_usuario: str
    
    id_plataforma: int
    nombre_plataforma: str
    id_usuario_en_plataforma: str

class CerrarSesionDTO(BaseModel):
    token_usuario: str

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#ENDPOINTS

#Endpoint para vincular un usuario a una plataforma    
@router.post("/vincular", status_code=status.HTTP_200_OK)
def vincular_usuario(datos: VincularUsuarioDTO):
    try:
        id_externo_usuario, token_usuario = plataformas_use_case.vincular_plataforma(
            nombre_usuario=datos.nombre_usuario,
            password_usuario=datos.password_usuario,
            id_plataforma=datos.id_plataforma,
            nombre_plataforma=datos.nombre_plataforma,
            id_usuario_en_plataforma=datos.id_usuario_en_plataforma)
        
        return {"status":"ok",
                "message": "Usuario vinculado correctamente",
                "token_usuario": token_usuario,
                "id_externo_usuario": id_externo_usuario
                }
    
        
    except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=str(e))
        
    except HTTPException:
        raise

    except Exception as e:
        print(f"Error en la vinculación: {str(e)}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error interno del servidor al procesar la vinculación."
        )

#Endpoint para cerrar la sesión de un usuario en una plataforma
@router.post("/cerrar_sesion", status_code=status.HTTP_200_OK)
def cerrar_sesion(datos: CerrarSesionDTO):
    try:
        plataformas_use_case.cerrar_sesion(token_usuario=datos.token_usuario)
        return {"message": "Sesión cerrada correctamente"}
    except Exception as e:
        print(f"Error al cerrar la sesión: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al procesar el cierre de sesión."
        )