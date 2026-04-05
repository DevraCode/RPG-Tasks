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
            SELECT u.id_interno, u.nombre_jugador 
            FROM usuarios u
            JOIN vinculaciones v ON u.id_interno = v.id_interno
            WHERE v.id_externo = %s AND v.plataforma = %s
        """
        cursor.execute(query, (str(id_ext), plataforma))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_interno=res['id_interno'], nombre_jugador=res['nombre_jugador'])
        return None

    def registrar_usuario_completo(self, usuario, plataforma, id_ext, personaje):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar en Usuarios
            cursor.execute("INSERT INTO usuarios (id_interno, nombre_jugador) VALUES (%s, %s)", 
                           (usuario.id_interno, usuario.nombre_jugador))
            
            # 2. Insertar en Vinculaciones (Telegram/Discord)
            cursor.execute("INSERT INTO vinculaciones (id_interno, plataforma, id_externo) VALUES (%s, %s, %s)", 
                           (usuario.id_interno, plataforma, str(id_ext)))
            
            # 3. Insertar en Personajes
            cursor.execute("INSERT INTO personajes (id_interno, clase) VALUES (%s, %s)", 
                           (personaje.id_interno, personaje.clase))
            
            conn.commit() # Confirmamos todos los cambios a la vez
        except Exception as e:
            conn.rollback() # Si algo falla, no se guarda nada (integridad)
            raise e
        finally:
            cursor.close()
            conn.close()