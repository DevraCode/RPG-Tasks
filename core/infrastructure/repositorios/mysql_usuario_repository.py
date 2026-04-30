import mysql.connector
from core.application.ports.usuarios_ports import UsuarioRepository
from core.domain.models import Usuario, Plataformas

class MySQLUsuarioRepository(UsuarioRepository):

    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    def buscar_por_id_usuario(self, id_usuario: str):
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

    def buscar_por_id_externo(self, id_externo_usuario: str):
        print(f"DEBUG: Buscando hash -> '{id_externo_usuario}' (Longitud: {len(id_externo_usuario)})")


        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        query = """
            SELECT u.id_usuario, u.nombre_usuario
            FROM usuarios u
            INNER JOIN plataformas p ON u.id_usuario = p.id_usuario
            WHERE p.id_externo_usuario = %s AND p.sesion_activa = 1
        """
        cursor.execute(query, (id_externo_usuario,))
        res = cursor.fetchone()

        
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], 
                           nombre_usuario=res['nombre_usuario'])
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------
    
    def buscar_usuario_por_nombre(self, nombre_usuario: str):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True)
    
        query = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario']
            )
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------

    def buscar_usuario_por_plataforma(self, plataforma:str):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True)
    
        query ="""
            SELECT u.id_usuario, u.nombre_usuario, p.nombre_plataforma
            FROM usuarios u
            INNER JOIN plataformas p ON u.id_usuario = p.id_usuario
            WHERE p.nombre_plataforma = %s
        """
        cursor.execute(query, (plataforma,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario'], 
                nombre_usuario=row['nombre_usuario']
            )
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------

    def buscar_usuario_en_bd(self, nombre_usuario):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True)

        query ="""
            SELECT u.id_usuario, u.nombre_usuario, u.password_usuario
            FROM usuarios u
            WHERE u.nombre_usuario = %s
        """

        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario'], 
                nombre_usuario=row['nombre_usuario'],
                password_usuario=row['password_usuario']
            )
        return None
    

    def comprobar_usuario_contraseña(self, nombre_usuario: str, password_usuario: str):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True)

        query ="""
            SELECT id_usuario, nombre_usuario, password_usuario
            FROM usuarios 
            WHERE nombre_usuario = %s AND password_usuario = %s
        """
        cursor.execute(query, (nombre_usuario,password_usuario))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario'],
                nombre_usuario=row['nombre_usuario'],
                password_usuario=row['password_usuario']
            )
        return None
    

    def registrar_usuario(self, usuario: Usuario, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ 
        INSERT INTO usuarios 
        (nombre_usuario, password_usuario, email_usuario, rango, tipo_usuario)
        VALUES (%s, %s, %s, %s, %s)
        """
        query2 = """ 
        INSERT INTO plataformas
        (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario)
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            usuario.nombre_usuario, 
            usuario.password_usuario, 
            usuario.email_usuario,
            usuario.rango,
            usuario.tipo_usuario
        )

        try:
            cursor.execute(query, valores)
            id_usuario = cursor.lastrowid #Guarda el id del usuario
            cursor.execute(query2, (id_plataforma, nombre_plataforma, id_usuario, id_externo_usuario))
            conn.commit()
            return id_usuario

        finally:
            cursor.close()
            conn.close()

   
    def buscar_usuario_ia(self, nombre_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario']
            )
        return None
    
