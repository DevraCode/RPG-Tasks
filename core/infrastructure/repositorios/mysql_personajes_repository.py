import mysql.connector
from core.application.ports.personajes_ports import PersonajesRepository
from core.domain.models import Personaje

class MySQLPersonajesRepository(PersonajesRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    def registrar_personaje_elegido(self, id_usuario, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje, descripcion_personaje):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ INSERT INTO personajes (id_usuario, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje, descripcion_personaje)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                """
        
        try:
            cursor.execute(query, (id_usuario,nombre_personaje,genero,clase,imagen_personaje,icono_personaje,animacion_personaje,descripcion_personaje,))
            conn.commit() 
        finally:
            cursor.close()
            conn.close()

    #-----------------------------------------------------------------------------------------------------------------------------

    #Para establecer un máximo de 5 personajes por usuario
    def limite_personajes_de_usuario(self, id_usuario):
        
        conn = self._get_connection() 
        cursor = conn.cursor(buffered=True)
        
        try:
            query = "SELECT COUNT(*) FROM personajes WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            total_personajes = cursor.fetchone()[0]

           
            return total_personajes < 5
            
        except Exception as e:
            print(f"Error contando personajes: {e}")
            return False
        finally:
            
            cursor.close()
            conn.close()

    #-----------------------------------------------------------------------------------------------------------------------------
    
    def lista_personajes_usuario(self, id_usuario):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = "SELECT * FROM personajes p WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        personajes = cursor.fetchall()

        cursor.close()
        conn.close()

        return personajes
    
    def vincular_id_personaje_con_usuario(self, id_externo_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        try:
            query1 = "SELECT id_usuario from plataformas WHERE id_externo_usuario = %s"
            cursor.execute(query1, (id_externo_usuario,))
            row1 = cursor.fetchone()

            if not row1:
                print(f"FALLO: No existe vínculo para el hash {id_externo_usuario}")
                return None

            id_interno = row1['id_usuario']
            

            
            query2 = "SELECT id_personaje FROM personajes WHERE id_usuario = %s"
            cursor.execute(query2, (id_interno,))
            row2 = cursor.fetchone()

            if row2:
                
                return {"id_usuario": id_interno, "id_personaje": row2['id_personaje']}
            
            return {"id_usuario": id_interno, "id_personaje": None}       
            
        finally:
            cursor.close()
            conn.close()
    

    