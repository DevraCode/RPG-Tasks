import hashlib
import secrets
from rpg_tasks.core.domain.entidades import Plataformas
from rpg_tasks.core.domain.auth_utils import generar_id_usuario_en_plataforma, generar_token_sesion



class PlataformasUseCase:
    def __init__(self, repo_plataformas, repo_usuarios):
        self.repo_plataformas = repo_plataformas
        self.repo_usuarios = repo_usuarios

    
    def vincular_plataforma(self,nombre_usuario, password_usuario, id_plataforma: int, nombre_plataforma: str, id_usuario_en_plataforma: str):
        
        nueva_plataforma = Plataformas(
            id_plataforma = id_plataforma,
            nombre_plataforma = nombre_plataforma
        )

        #Primero comprobamos que el usuario y la contraseña coinciden
        usuario = self.repo_usuarios.autenticar_usuario(nombre_usuario)
        password = usuario["password_usuario"] #Sacado de la BD

        password_hasheado = hashlib.sha256(str(password_usuario).encode()).hexdigest()[:8] #Debe coincidir con el password encriptado de la BD


        if not usuario:
            raise ValueError("El nombre de usuario no existe.")
        
        if password != password_hasheado:
            raise ValueError("La contraseña es incorrecta.")
        
        #Si coinciden, comprobamos si el token_usuario ya está vinculado a un usuario
        else:

            id_usuario = usuario["id_usuario"]
            id_externo_usuario = usuario["id_externo_usuario"]
        
            token_usuario = generar_token_sesion()

            id_usuario_en_plataforma_hash = generar_id_usuario_en_plataforma(id_usuario_en_plataforma)

            #Hay que comprobar si existe este id en la tabla plataformas. Diferenciar entre el id del usuario normal y el id del usuario dentro de la plataforma
            id_usuario_en_plataforma_existe = self.repo_plataformas.id_usuario_en_plataforma_existe(id_usuario_en_plataforma_hash)
            
            #Si existe quiere decir que ya está vinculado
            if id_usuario_en_plataforma_existe:
                raise ValueError("Ya existe una cuenta vinculada a esta aplicación. Cierra la sesión antes de vincular una cuenta primero")
            
            #Si no está vinculado, procedemos a vincularlo
            else: 
                vinculacion = self.repo_plataformas.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_usuario, token_usuario, id_usuario_en_plataforma_hash)
                return True