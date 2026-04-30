from core.domain.models import Usuario

class UsuarioUsecase:
    def __init__(self, repo):
        self.repo = repo

    def registrar_usuario(self, nombre_usuario: str, password_usuario: str, email_usuario: str, rango: str, tipo_usuario:int, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        nuevo_usuario = Usuario(
            id_usuario = None,
            nombre_usuario = nombre_usuario,
            password_usuario = password_usuario,
            email_usuario = email_usuario,
            rango = rango,
            tipo_usuario = tipo_usuario

        )
        registro = self.repo.registrar_usuario(nuevo_usuario, id_plataforma, nombre_plataforma, id_externo_usuario)
        return registro
    
    def id_usuario_existe(self, id_usuario: int):
        usuario = self.repo.buscar_por_id_usuario(id_usuario)
        
        return usuario
    
    def nombre_usuario_existe(self, nombre_usuario: str):
        usuario = self.repo.buscar_usuario_en_bd(nombre_usuario)
        if usuario:
            mensaje = "Ese usuario ya existe"
            return mensaje
        
    def id_externo(self, id_externo_usuario: str):
        usuario = self.repo.buscar_usuario_en_bd(id_externo_usuario)
        return usuario
    
    def buscar_usuario_por_nombre(self, nombre_usuario: str):
        resultado = self.repo.buscar_usuario_por_nombre(nombre_usuario)
        return resultado
    
    def buscar_id_externo_usuario(self, id_externo):
        usuario = self.repo.buscar_por_id_externo(id_externo)
        return usuario


    def comprobar_usuario(self, nombre_usuario:str, password_usuario:str):
        resultado = self.repo.comprobar_usuario_contraseña(nombre_usuario, password_usuario)
        return resultado
    
    def buscar_usuario_ia(self, nombre_usuario:str):
        """Busca el ID del usuario por su nombre."""
        
        resultado = self.repo.buscar_usuario_ia(nombre_usuario)
        return resultado.id_usuario

