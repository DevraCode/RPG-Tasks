

class UsuarioIAUsecase:
    def __init__(self, repo):
        self.repo = repo
    
    def buscar_usuario_ia(self, nombre_usuario:str):
        """Busca el ID del usuario por su nombre."""
        
        resultado = self.repo.buscar_usuario_ia(nombre_usuario)
        return resultado.id_usuario
    

