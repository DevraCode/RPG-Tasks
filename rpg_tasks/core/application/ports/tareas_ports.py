from abc import ABC, abstractmethod


class TareasRepository(ABC):
    @abstractmethod
    def insertar_tarea(self, id_usuario, nombre_tarea):
        pass

    @abstractmethod
    def lista_tareas_usuario(self,id_usuario):
        pass

    @abstractmethod
    def lista_tareas_usuario_completadas(self,id_usuario):
        pass

    @abstractmethod
    def buscar_tarea_usuario(self,id_usuario):
        pass

    @abstractmethod
    def completar_tarea(self, id_tarea):
        pass

    @abstractmethod
    def buscar_tarea_por_id(self, id_tarea):
        pass

    @abstractmethod
    def vincular_id_personaje_con_id_tarea(self, id_personaje, id_tarea):
        pass
