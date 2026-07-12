import hashlib
import secrets
from rpg_tasks.core.domain.entidades import Plataformas



class PlataformasUseCase:
    def __init__(self, repo_plataformas, repo_usuarios):
        self.repo_plataformas = repo_plataformas
        self.repo_usuarios = repo_usuarios

    
    def vincular_plataforma(self,nombre_usuario, password_usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        
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

            id_externo_generado = hashlib.sha256(str(id_externo_usuario).encode()).hexdigest()[:8]
            id_externo_usuario_existe = self.repo_plataformas.id_externo_usuario_existe(id_externo_generado)

            token_generado = secrets.token_hex(16)
            token_usuario = hashlib.sha256(str(token_generado).encode()).hexdigest()[:8]


            #Si id ya esta vinculado
            if id_externo_usuario_existe:
                raise ValueError("Ya existe una cuenta vinculada a esta aplicación. Cierra la sesión antes de vincular una cuenta primero")
            
            #Si no está vinculado, procedemos a vincularlo
            else: 
                vinculacion = self.repo_plataformas.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_generado, token_usuario)
                return True