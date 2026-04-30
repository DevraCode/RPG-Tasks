import mysql.connector
from core.application.ports import TareasRepository
from core.domain.models import Tareas

class MySQLTareasRepository(TareasRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    
    def insertar_tarea(self, id_usuario, nombre_tarea):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        query = "INSERT INTO tareas (id_usuario, nombre_tarea) VALUES (%s, %s)"

        cursor.execute(query, (id_usuario, nombre_tarea,))
        conn.commit()
        cursor.close()
        conn.close()
   
