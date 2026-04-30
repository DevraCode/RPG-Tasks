class TareasUseCase:
    def __init__(self, repo):
        self.repo = repo

    def insertar_tarea(self, id_usuario, nombre_tarea):

        nombre_tarea_minusculas = nombre_tarea.lower()
        self.repo.insertar_tarea(id_usuario, nombre_tarea_minusculas)

        mensaje = f"Tarea {nombre_tarea_minusculas.capitalize()} añadida correctamente "

        return mensaje