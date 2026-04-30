import uuid
import hashlib
import inspect
from core.domain.models import Usuario, Plataformas
from core.domain.auth_utils import verificar_password
from core.domain.clases_personajes import CLASES_DISPONIBLES


class PlataformasUseCase:
    def __init__(self, repo):
        self.repo = repo

    def usuario_activo(self, id_externo_usuario):

        sesion = self.repo.obtener_estado_sesion(id_externo_usuario)
        
        return sesion
    
    def vincular_id_externo_usuario(self, id_externo):
        resultado = self.repo.vincular_id_externo_con_interno(id_externo)

        return resultado
    
    

    def vincular_plataforma(self, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str, id_usuario: int):
        nueva_plataforma = Plataformas(
            id_plataforma = id_plataforma,
            nombre_plataforma = nombre_plataforma
        )

        vinculacion = self.repo.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_usuario)
        return vinculacion