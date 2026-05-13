from core.domain.logica_tareas import LogicaTareas


class TareasUseCase:
    def __init__(self, repo):
        self.repo = repo

    def insertar_tarea(self, id_usuario, nombre_tarea):

        nombre_tarea_minusculas = nombre_tarea.lower()
        self.repo.insertar_tarea(id_usuario, nombre_tarea_minusculas)

        mensaje = f"Tarea {nombre_tarea_minusculas.capitalize()} añadida correctamente "

        return mensaje
    
    def lista_tareas_usuario(self, id_usuario):
        lista = self.repo.lista_tareas_usuario(id_usuario)
        return lista
    
    def buscar_tarea_por_id(self, id_tarea):
        tarea = self.repo.buscar_tarea_por_id(id_tarea)
        return tarea
    
    def completar_tarea(self,id_tarea):
        self.repo.completar_tarea(id_tarea)
    
    def vincular_personaje_con_tarea(self, id_personaje, id_tarea):
        self.repo.vincular_id_personaje_con_id_tarea(id_personaje, id_tarea)

    def temporizador(self, minutos):
        logica_tareas = LogicaTareas()
        logica_tareas.temporizador(minutos)
    
    def experiencia_tarea_completada(self):
        logica_tareas = LogicaTareas()
        return logica_tareas.tarea_completada()
        