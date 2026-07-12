from rpg_tasks.core.domain.entidades import Plataformas



class PlataformasUseCase:
    def __init__(self, repo_plataformas, repo_usuarios):
        self.repo_plataformas = repo_plataformas
        self.repo_usuarios = repo_usuarios

    
    def vincular_plataforma(self,nombre_usuario, password_usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str, id_usuario: int):
        
        nueva_plataforma = Plataformas(
            id_plataforma = id_plataforma,
            nombre_plataforma = nombre_plataforma
        )

        #Primero comprobamos que el usuario y la contraseña coinciden
        usuario = self.repo_usuarios.autenticar_usuario(nombre_usuario)

        if not usuario:
            raise ValueError("El nombre de usuario no existe.")
        
        if usuario["password_usuario"] != password_usuario:
            raise ValueError("La contraseña es incorrecta.")
        
        #Si coinciden, comprobamos si el id_externo_usuario ya está vinculado a un usuario
        else:

            id_usuario = usuario["id_usuario"]
            id_externo_existe = self.repo_plataformas.id_externo_existe(id_usuario)

            if id_externo_existe:
                raise ValueError("Este usuario ya está vinculado")
            
            #Si no está vinculado, procedemos a vincularlo
            else: 
                vinculacion = self.repo_plataformas.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_usuario)
                return True