

class UsuarioIAUsecase:
    def __init__(self, repo):
        self.repo = repo
    
    def buscar_usuario_ia(self, nombre_usuario:str):
        """Busca el ID del usuario por su nombre. Si el usuario no existe en la base de datos, reponde con 'Ese usuario no existe'"""
        
        resultado = self.repo.buscar_usuario_ia(nombre_usuario)
        
        if resultado:
            return f"El ID del usuario en la base de datos es: {resultado.id_usuario}"
        
        return "Ese usuario no existe"
    

