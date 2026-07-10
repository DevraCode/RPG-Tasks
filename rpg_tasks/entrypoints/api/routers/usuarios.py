
#IMPORTACIONES
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
#-----------------------------------------------------------------------------------------------------------------------------
from rpg_tasks.infrastructure.dbconfig import db_config
from rpg_tasks.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from rpg_tasks.core.application.use_cases.usuarios_use_cases import UsuarioUseCase
from rpg_tasks.core.domain.auth_utils import decodificar_id_usuario

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INICIALIZACIÓN DE REPOSITORIOS Y CASOS DE USO
repo_usuario = MySQLUsuarioRepository(db_config)
usuario_use_case = UsuarioUseCase(repo_usuario)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Router de FastAPI para los endpoints relacionados con usuarios
router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"])

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#DTOs

#DTO para el registro de usuarios
class RegistroUsuarioDTO(BaseModel):
    id_usuario: int = None
    id_externo_usuario: str = "0"
    nombre_usuario: str = None
    password_usuario: str = None
    email_usuario : str = None
    fecha_registro: datetime = None
    activo: bool = True
    rango: str = None
    tipo_usuario: int = 0
    idioma_usuario: str = None
    id_plataforma: int = None
    nombre_plataforma: str = None
    id_externo_usuario: str = None   


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#ENDPOINTS
#Busca a un usuario por su Id. Para la url, esta id estará codificada por seguridad, y se decodificará en el endpoint antes de buscar al usuario en la base de datos.
@router.get("/buscar/{id_usuario_codificada}")
def buscar_usuario(id_usuario_codificada):

    try:
        id_usuario_real = decodificar_id_usuario(id_usuario_codificada)
        usuario = usuario_use_case.buscar_usuario_por_id(id_usuario_real)
        return {
            "status": "ok",
            "data": usuario
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 
#Endpoint para registrar un nuevo usuario    
@router.post("/registro")
def registrar_usuario(datos: RegistroUsuarioDTO):
    try:
        
        usuario_creado = usuario_use_case.registrar_usuario(
            nombre_usuario=datos.nombre_usuario,
            password_usuario=datos.password_usuario,
            email_usuario=datos.email_usuario,
            rango=datos.rango,
            tipo_usuario=datos.tipo_usuario,
            idioma_usuario=datos.idioma_usuario,
            id_plataforma=datos.id_plataforma,
            nombre_plataforma=datos.nombre_plataforma,
            id_externo_usuario=datos.id_externo_usuario)
        
        return {
            "status": "ok",
            "message": "Usuario registrado correctamente"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar: {str(e)}")
    
#Endpoint para verificar si un nombre de usuario ya está registrado en la base de datos. Devuelve un mensaje indicando si el nombre está disponible o no.
@router.get("/verificar-nombre/{nombre}")
def verificar_nombre(nombre: str):
    existe = usuario_use_case.nombre_usuario_existe(nombre)
    
    if existe:
        raise HTTPException(status_code=400, detail="Ese nombre de usuario ya está registrado.")
    
    return {"status": "disponible", "message": "El nombre está libre"}