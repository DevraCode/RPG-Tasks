import hashlib
import secrets

from rpg_tasks.core.domain.entidades import Usuario

class UsuarioUseCase:
    def __init__(self, repo_usuarios, repo_plataformas):
        self.repo = repo_usuarios
        self.repo_plataformas = repo_plataformas

    def buscar_usuario_por_id(self, id_usuario: str):
        usuario = self.repo.buscar_usuario_por_id(id_usuario)
        return usuario
    
    def nombre_usuario_existe(self, nombre_usuario: str):
        usuario = self.repo.nombre_usuario_existe(nombre_usuario)
        return usuario
    


    def registrar_usuario(self, nombre_usuario: str, password_usuario: str, email_usuario: str, rango: str, tipo_usuario:int, idioma_usuario: str, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        
        password_bytes = f"{password_usuario}".encode()
        password_encriptado = hashlib.sha256(password_bytes).hexdigest()[:8]

        id_externo_generado = hashlib.sha256(str(id_externo_usuario).encode()).hexdigest()[:8]
        
        nuevo_usuario = Usuario(
            id_usuario = None,
            nombre_usuario = nombre_usuario,
            password_usuario = password_encriptado,
            email_usuario = email_usuario,
            rango = rango,
            tipo_usuario = tipo_usuario,
            idioma_usuario= idioma_usuario

        )


        nombre_usuario_existe = self.repo.nombre_usuario_existe(nombre_usuario)
        id_externo_usuario_existe = self.repo_plataformas.id_externo_usuario_existe(id_externo_generado)

        token_generado = secrets.token_hex(16)
        token_usuario = hashlib.sha256(str(token_generado).encode()).hexdigest()[:8]


        #Comprobar si el nombre de usuario ya existe antes de registrar al usuario
        if nombre_usuario_existe:
            raise ValueError("El nombre de usuario ya existe.")
        
        #Comprobar si el id_externo_usuario ya está en la base de datos
        if id_externo_usuario_existe:
            raise ValueError("El usuario ya está registrado en esta plataforma. Cierra la sesión para poder registrarte de nuevo.")


        registro = self.repo.registrar_usuario(nuevo_usuario, id_plataforma, nombre_plataforma, id_externo_generado, token_usuario)
        return registro
    
    
    

   
    
