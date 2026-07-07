

class PersonajesIAUsecase:
    def __init__(self, repo_usuarios, repo_personajes):
        self.repo_usuarios = repo_usuarios
        self.repo_personajes = repo_personajes
    
    def descripcion_personaje(self, id_usuario: int):
        """Crea una descripcion detallada del personaje que pertenezca al usuario a partir del nombre del personaje"""
        

        lista = self.repo_personajes.lista_personajes_usuario(id_usuario)

        datos_para_ia = []
        for p in lista:
            datos_para_ia.append({
                "nombre": p.nombre_personaje,
                "clase": p.clase_personaje,
                "nivel": p.nivel,
                "fuerza": p.fuerza
            })

        return datos_para_ia
    

