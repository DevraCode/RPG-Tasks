import mysql.connector
from core.application.ports import PlataformasRepository
from core.domain.models import Plataformas

class MySQLPlataformasRepository(PlataformasRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #Para Telegram / Discord - Busca a que usuario pertenece su id externo
    def vincular_id_externo_con_interno(self, id_externo_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True) 
        try:
            query = "SELECT id_usuario FROM plataformas WHERE id_externo_usuario = %s"
            cursor.execute(query, (id_externo_usuario,))
            row = cursor.fetchone()
            
            if row:
                
                return row['id_usuario']
            
            
            return None
        finally:
            cursor.close()
            conn.close()


    #Vincula la plataforma al iniciar sesión en otro lugar
    def vincular_plataforma(self, plataformas: Plataformas, id_usuario, id_externo_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """ 
        INSERT INTO plataformas 
        (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario)
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            plataformas.id_plataforma,
            plataformas.nombre_plataforma,
            id_usuario,
            id_externo_usuario
        )

        try:
            cursor.execute(query, valores)
            conn.commit()
            

        finally:
            cursor.close()
            conn.close()

    def obtener_estado_sesion(self, id_externo_usuario):

        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True) 

        query = """
        SELECT sesion_activa
        FROM plataformas
        WHERE id_externo_usuario = %s AND sesion_activa = 1
        """
        
        try:
            cursor.execute(query, (id_externo_usuario,))
            resultado = cursor.fetchone()

            
            if resultado:
                return bool(resultado['sesion_activa'])
            
            return False 

        finally:
            
            cursor.close()
            conn.close()

    def iniciar_sesion(self, id_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """ UPDATE plataformas
                    SET sesion_activa = 1
                    WHERE p.id_usuario =  %s """

        try:
            cursor.execute(query, (id_usuario,))
            conn.commit() 
        finally:
            cursor.close()
            conn.close()


    def cerrar_sesion(self, id_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """ UPDATE plataformas
                    SET sesion_activa = 0
                    WHERE p.id_usuario =  %s """

        try:
            cursor.execute(query, (id_usuario,))
            conn.commit() 
        finally:
            cursor.close()
            conn.close()



    def sesion_cerrada(self, id_externo_usuario):
        pass


