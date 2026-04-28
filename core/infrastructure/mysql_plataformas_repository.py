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
            
            print(f"FALLO: No existe ninguna fila con el hash {id_externo_usuario} en la tabla plataformas")
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

    def obtener_estado_sesion(self, id_usuario):

        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT sesion_activa
        FROM plataformas
        WHERE id_usuario = %s
        """
        
        try:
            cursor.execute(query, (id_usuario,))
            resultado = cursor.fetchone()

            return bool(resultado['sesion_activa'])

        finally:
            cursor.close()
            conn.close()