import hashlib
import bcrypt
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

        #Comprobamos que el usuario existe
        if not usuario:
            raise ValueError("El nombre de usuario no existe.")

        #Si existe, sacamos la contraseña
        password = usuario["password_usuario"] #Sacado de la BD

        password_bytes = password_usuario.encode('utf-8')
        password_db_bytes = password.encode('utf-8') #El hash almacenado en la DB

        #Ahora comprobamos que la contraseña coincida
        if not bcrypt.checkpw(password_bytes, password_db_bytes):
            raise ValueError("La contraseña es incorrecta.")


        #Si coinciden, comprobamos si el token_usuario ya está vinculado a un usuario
        else:

            id_usuario = usuario["id_usuario"]
            id_externo_usuario = usuario["id_externo_usuario"]
        
            token_usuario = generar_token_sesion()
            token_usuario_hash = hashlib.sha256(token_usuario.encode()).hexdigest()[:8]

            id_usuario_en_plataforma_hash = generar_id_usuario_en_plataforma(id_usuario_en_plataforma)

            #Hay que comprobar si existe este id en la tabla plataformas. Diferenciar entre el id del usuario normal y el id del usuario dentro de la plataforma
            #El id del usuario en la plataforma es un id único del usuario en esa plataforma. Sirve para evitar cuentas duplicadas.
            id_usuario_en_plataforma_existe = self.repo_plataformas.id_usuario_en_plataforma_existe(id_usuario_en_plataforma_hash)
            
            #Si existe quiere decir que ya está vinculado
            if id_usuario_en_plataforma_existe:
                raise ValueError("Ya existe una cuenta vinculada a esta aplicación. Cierra la sesión antes de vincular una cuenta primero")
            
            #Si no está vinculado, procedemos a vincularlo
            else: 
                vinculacion = self.repo_plataformas.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_usuario, token_usuario_hash, id_usuario_en_plataforma_hash)
                return id_externo_usuario, token_usuario


    def cerrar_sesion(self, token_usuario: str):
        #Cierra la sesión del usuario en la plataforma
        token_usuario_hash = hashlib.sha256(token_usuario.encode()).hexdigest()[:8]
        self.repo_plataformas.cerrar_sesion(token_usuario_hash)
        return True
        