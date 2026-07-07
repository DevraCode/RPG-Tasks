import mysql.connector
from core.application.ports.tareas_ports import TareasRepository
from core.domain.entidades import Tareas

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
   
    def lista_tareas_usuario(self,id_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM tareas WHERE id_usuario = %s"

        cursor.execute(query,(id_usuario,))
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultados
    
    def lista_tareas_usuario_completadas(self, id_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM tareas WHERE id_usuario = %s AND tarea_completada = TRUE"

        cursor.execute(query,(id_usuario,))
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultados

    def buscar_tarea_usuario(self,id_usuario):
        pass
    
    def completar_tarea(self, id_tarea):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "UPDATE tareas SET tarea_completada = TRUE WHERE id_tarea = %s"

        cursor.execute(query,(id_tarea,))

        conn.commit()

        
        
        cursor.close()
        conn.close()
        

    def buscar_tarea_por_id(self, id_tarea):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM tareas WHERE id_tarea = %s"

        cursor.execute(query,(id_tarea,))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado
    
    def vincular_id_personaje_con_id_tarea(self, id_personaje, id_tarea):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "UPDATE tareas SET id_personaje = %s WHERE id_tarea = %s"

        cursor.execute(query,(id_personaje, id_tarea,))

        conn.commit()
        
        cursor.close()
        conn.close()

        