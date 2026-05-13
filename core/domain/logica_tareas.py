from datetime import datetime, timedelta


class LogicaTareas:
    def __init__(self):
         pass
    
    def tarea_completada(self):
         return 150
    
    def temporizador(self,minutos: int):
         return datetime.now() + timedelta(minutes=minutos)