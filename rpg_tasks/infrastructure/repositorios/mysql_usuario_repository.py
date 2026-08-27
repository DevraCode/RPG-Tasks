import mysql.connector
from rpg_tasks.core.application.output_ports.usuarios_ports import UsuarioRepository
from rpg_tasks.core.domain.entidades import Usuario


class MySQLUsuarioRepository(UsuarioRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    def buscar_usuario_por_id(self, id_usuario: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT *
                    FROM usuarios u
                    WHERE u.id_usuario = %s"""
        
        cursor.execute(query, (id_usuario,))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], 
                           nombre_usuario=res['nombre_usuario'])
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------

    def buscar_usuario_por_id_plataforma(self,id_usuario_en_plataforma):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT *
                    FROM plataformas p
                    WHERE p.id_usuario_en_plataforma = %s"""
        
        cursor.execute(query, (id_usuario_en_plataforma,))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], 
                           id_externo_usuario=res['id_externo_usuario'])
        return None

    #-----------------------------------------------------------------------------------------------------------------------------
    def buscar_usuario_por_token(self, token_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT *
                    FROM plataformas p
                    INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
                    WHERE p.token_usuario = %s"""
        
        cursor.execute(query, (token_usuario,))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], 
                           id_externo_usuario=res['id_externo_usuario'])
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------

    def nombre_usuario_existe(self, nombre_usuario: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT 1 FROM usuarios WHERE nombre_usuario = %s LIMIT 1"
        
        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone() 
        
        cursor.close()
        conn.close()

        return True if row else False
      
    #-----------------------------------------------------------------------------------------------------------------------------

    def registrar_usuario(self, usuario: Usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario:str, token_usuario: str, id_usuario_en_plataforma: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ 
        INSERT INTO usuarios 
        (id_externo_usuario, nombre_usuario, password_usuario, email_usuario, idioma_usuario)
        VALUES (%s, %s, %s, %s, %s)
        """
        query2 = """ 
        INSERT INTO plataformas
        (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario, token_usuario, id_usuario_en_plataforma)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario.id_externo_usuario,
            usuario.nombre_usuario, 
            usuario.password_usuario, 
            usuario.email_usuario,
            usuario.idioma_usuario
        )

        try:
            cursor.execute(query, valores)
            id_usuario = cursor.lastrowid #Guarda el id del usuario
            id_externo_usuario = usuario.id_externo_usuario #Guarda el id_externo_usuario
            cursor.execute(query2, (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario, token_usuario, id_usuario_en_plataforma))
            conn.commit()
            return usuario

        finally:
            cursor.close()
            conn.close()

    #-----------------------------------------------------------------------------------------------------------------------------
   
    def autenticar_usuario(self, nombre_usuario: str):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True)

        query ="""
            SELECT *
            FROM usuarios 
            WHERE nombre_usuario = %s
        """
        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return row

        return None
    

    

   
    