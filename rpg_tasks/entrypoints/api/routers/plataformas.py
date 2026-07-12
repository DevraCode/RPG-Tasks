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
        vincular = plataformas_use_case.vincular_plataforma(
            nombre_usuario=datos.nombre_usuario,
            password_usuario=datos.password_usuario,
            id_plataforma=datos.id_plataforma,
            nombre_plataforma=datos.nombre_plataforma,
            token_usuario=datos.token_usuario)
        
        return {"message": "Usuario vinculado correctamente"}
    
        
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