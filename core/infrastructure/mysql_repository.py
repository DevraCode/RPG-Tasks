# core/infrastructure/mysql_repository.py
import mysql.connector
from core.application.ports import UsuarioRepository
from core.domain.models import Usuario, Personaje

class MySQLUsuarioRepository(UsuarioRepository):
    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)

    def buscar_por_id_externo(self, id_ext: str, plataforma: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT u.id_usuario, u.nombre_usuario, u.password_usuario
            FROM usuarios u
            JOIN plataformas p ON u.id_usuario = p.id_usuario
            WHERE p.id_externo_usuario = %s AND p.nombre_plataforma = %s
        """
        cursor.execute(query, (str(id_ext), plataforma))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], nombre_usuario=res['nombre_usuario'], password_usuario=res['password_usuario'])
        return None
    
    def buscar_usuario_por_nombre(self, nombre_usuario: str):
        conn = self._get_connection() # Usamos tu método auxiliar
        cursor = conn.cursor(dictionary=True)
    
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
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


    #Registra al usuario con su id, nombre, contraseña, plataforma y personaje
    def registrar_usuario_completo(self, usuario, plataforma, id_ext, personaje):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Insertar en la tabla Usuarios
            cursor.execute("INSERT INTO usuarios (id_usuario, nombre_usuario, password_usuario) VALUES (%s, %s, %s)", 
                           (usuario.id_usuario, usuario.nombre_usuario, usuario.password_usuario))
            
            # Insertar en la tabla Plataformas
            cursor.execute("INSERT INTO plataformas (id_usuario, nombre_plataforma, id_externo_usuario) VALUES (%s, %s, %s)", 
                           (usuario.id_usuario, plataforma, str(id_ext)))
            
            # Insertar en la tabla Personajes
            cursor.execute("INSERT INTO personajes (id_usuario) VALUES (%s)", 
                           [personaje.id_usuario])
            
            conn.commit() 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()


    def sesion_iniciada(self, nombre_usuario):
        conn = self._get_connection()
        cursor = conn.cursor()

        query ="""
            SELECT u.id_usuario, u.nombre_usuario, u.activo
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
                activo=row['activo']
            )
        return None

