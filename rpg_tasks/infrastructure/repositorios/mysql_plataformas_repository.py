import mysql.connector
from rpg_tasks.core.application.output_ports.plataformas_ports import PlataformasRepository
from rpg_tasks.core.domain.entidades import Plataformas

class MySQLPlataformasRepository(PlataformasRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    def id_externo_usuario_existe(self, id_externo_usuario: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT 1 FROM plataformas WHERE id_externo_usuario = %s LIMIT 1"
        
        cursor.execute(query, (id_externo_usuario,))
        row = cursor.fetchone() 
        
        cursor.close()
        conn.close()

        return True if row else False
    

    def id_externo_usuario_en_plataforma_existe(self, id_usuario_en_plataforma):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT 1 FROM plataformas WHERE id_usuario_en_plataforma = %s LIMIT 1"
        
        cursor.execute(query, (id_usuario_en_plataforma,))
        row = cursor.fetchone() 
        
        cursor.close()
        conn.close()

        return True if row else False

    
    def token_existe(self, token_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True) 
        try:
            query = "SELECT token_usuario FROM plataformas WHERE id_usuario = %s"
            cursor.execute(query, (token_usuario,))
            row = cursor.fetchone()
            
            if row:
                return row["token_usuario"]
            
            return None
        
        finally:
            cursor.close()
            conn.close()


    #Vincula la plataforma al iniciar sesión en otro lugar
    def vincular_plataforma(self, plataformas: Plataformas, id_usuario: int, id_externo_usuario: str, token_usuario: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """ 
        INSERT INTO plataformas 
        (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario, token_usuario)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            plataformas.id_plataforma,
            plataformas.nombre_plataforma,
            id_usuario,
            id_externo_usuario,
            token_usuario
        )

        try:
            cursor.execute(query, valores)
            conn.commit()
            

        finally:
            cursor.close()
            conn.close()

    

