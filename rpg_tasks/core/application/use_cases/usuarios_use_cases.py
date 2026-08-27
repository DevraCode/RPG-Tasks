import hashlib
import bcrypt

from rpg_tasks.core.domain.entidades import Usuario, CorrespondenciaPlataformas
from rpg_tasks.core.domain.auth_utils import generar_id_externo, generar_id_usuario_en_plataforma, generar_token_sesion

class UsuarioUseCase:
    def __init__(self, repo_usuarios, repo_plataformas):
        self.repo = repo_usuarios
        self.repo_plataformas = repo_plataformas

    def buscar_usuario_por_id(self, id_usuario: str):
        usuario = self.repo.buscar_usuario_por_id(id_usuario)
        return usuario
    
    def buscar_usuario_por_id_plataforma(self, id_usuario_en_plataforma):
        usuario = self.repo.buscar_usuario_por_id_plataforma(id_usuario_en_plataforma)
        return usuario

    def buscar_usuario_por_token(self, token_usuario):
        token_hash = hashlib.sha256(token_usuario.encode()).hexdigest()[:8]
        usuario = self.repo.buscar_usuario_por_token(token_hash)
        return usuario

    def nombre_usuario_existe(self, nombre_usuario: str):
        usuario = self.repo.nombre_usuario_existe(nombre_usuario)
        return usuario
    

    def registrar_usuario(self, nombre_usuario: str, password_usuario: str, email_usuario: str, idioma_usuario: str, id_plataforma: int, identificacion_plataforma: str):

        nombre_usuario_existe = self.repo.nombre_usuario_existe(nombre_usuario)

        """El parámetro identificacion plataforma se le pasará al endpoint de registro desde cada una de las plataformas.
            En el caso de Telegram es el chat_id, en Android es el android_id...etc. 
            Así se evita que un usuario tenga múltiples cuentas en un mismo dispositivo"""
        
        id_usuario_en_plataforma_hasheado = generar_id_usuario_en_plataforma(identificacion_plataforma)
        id_usuario_en_plataforma_existe = self.repo_plataformas.id_usuario_en_plataforma_existe(id_usuario_en_plataforma_hasheado)

        #Comprobar si el nombre de usuario ya existe antes de registrar al usuario
        if nombre_usuario_existe:
            raise ValueError("El nombre de usuario ya existe.")

        #Comprobar que el email no esté ya en uso
                
        #Comprobar si el id_externo_usuario ya está en la base de datos. Esto evita las multicuentas en la misma plataforma. Por ejemplo, un usuario no puede registrarse dos veces en Telegram con el mismo chat_id.
        if id_usuario_en_plataforma_existe:
            raise ValueError("El usuario ya está registrado en esta plataforma. Puedes iniciar sesión y borrar la cuenta de esta plataforma si quieres hacerte un usuario nuevo o iniciar sesion con otra cuenta.")


        password_bytes = password_usuario.encode('utf-8')
        password_encriptado = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        id_externo_generado = generar_id_externo()

        nuevo_usuario = Usuario(
            id_usuario = None,
            id_externo_usuario=id_externo_generado,
            nombre_usuario = nombre_usuario,
            password_usuario = password_encriptado,
            email_usuario = email_usuario,
            idioma_usuario= idioma_usuario)

        token_usuario = generar_token_sesion()
        token_usuario_hash = hashlib.sha256(token_usuario.encode()).hexdigest()[:8]
        nombre_plataforma = CorrespondenciaPlataformas(id_plataforma).name

        registro = self.repo.registrar_usuario(nuevo_usuario, id_plataforma, nombre_plataforma, id_externo_generado, token_usuario_hash, id_usuario_en_plataforma_hasheado)

        return registro, token_usuario
    
    
    

   
    
