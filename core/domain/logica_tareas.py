from datetime import datetime, timedelta


class LogicaTareas:
    def __init__(self):
         pass
    
    def tarea_completada(exp):
         return exp + 150
    
    def temporizador(minutos: int):
         return datetime.now() + timedelta(minutes=minutos)