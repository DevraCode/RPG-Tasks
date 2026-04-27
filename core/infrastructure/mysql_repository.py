import mysql.connector
from core.application.ports import UsuarioRepository
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
    #BUSCAR USUARIO

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

    def buscar_por_id_externo(self, id_externo_usuario: str, nombre_plataforma: str):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT u.id_usuario, u.nombre_usuario, u.password_usuario, p.id_externo_usuario
            FROM usuarios u
            JOIN plataformas p ON u.id_usuario = p.id_usuario
            WHERE p.id_externo_usuario = %s AND p.nombre_plataforma = %s
        """
        cursor.execute(query, (id_externo_usuario,nombre_plataforma,))
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res:
            return Usuario(id_usuario=res['id_usuario'], 
                           nombre_usuario=res['nombre_usuario'], 
                           password_usuario=res['password_usuario'],
                           id_externo_usuario=res['id_externo_usuario'])
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------
    
    def buscar_usuario_por_nombre(self, nombre_usuario: str):
        conn = self._get_connection() 
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

   

    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #PERSONAJES

    def registrar_personaje_elegido(self, id_usuario, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ INSERT INTO personajes (id_usuario, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        
        try:
            cursor.execute(query, (id_usuario,nombre_personaje,genero,clase,imagen_personaje,icono_personaje,animacion_personaje,))
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
    

    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #TAREAS

    def insertar_tarea(self, id_usuario, nombre_tarea):
        conn = self._get_connection() 
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        query = "INSERT INTO tareas (id_usuario, nombre_tarea) VALUES (%s, %s)"

        cursor.execute(query, (id_usuario, nombre_tarea,))
        conn.commit()
        cursor.close()
        conn.close()
   

    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #SESIONES

    def iniciar_sesion(self, id_externo_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        
        query = """ UPDATE usuarios u
                    JOIN plataformas p ON u.id_usuario = p.id_usuario
                    SET u.activo = 1
                    WHERE p.id_externo_usuario =  %s """

        try:
            cursor.execute(query, (id_externo_usuario,))
            conn.commit() 
        finally:
            cursor.close()
            conn.close()
        
    #-----------------------------------------------------------------------------------------------------------------------------

    def obtener_estado_sesion(self, id_externo_usuario, nombre_plataforma):

        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT u.activo 
        FROM usuarios u
        JOIN plataformas p ON u.id_usuario = p.id_usuario
        WHERE p.id_externo_usuario = %s 
          AND p.nombre_plataforma = %s
        LIMIT 1
        """
        
        try:
            cursor.execute(query, (id_externo_usuario,nombre_plataforma,))
            resultado = cursor.fetchone()
            
            return resultado is not None and resultado['activo'] == 1
        finally:
            cursor.close()
            conn.close()
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def cerrar_sesion(self, id_externo_usuario):
        pass

    #-----------------------------------------------------------------------------------------------------------------------------

    def sesion_cerrada(self, id_externo_usuario):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        query ="""
            SELECT u.id_usuario, u.nombre_usuario, u.activo, p.id_externo_usuario
            FROM usuarios u, plataformas p
            WHERE p.id_externo_usuario = %s AND u.activo = 0
        """
        cursor.execute(query, (id_externo_usuario,))
        row = cursor.fetchone()
        
        
        cursor.close()
        conn.close()

        if row:
            return Usuario(
                id_usuario=row['id_usuario'],
                id_externo_usuario=row["id_externo_usuario"],
                nombre_usuario=row['nombre_usuario'],
                activo=row['activo'] 
            )
        return None
    
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------
    # TELEGRAM / DISCORD

    #Registra al usuario con su id, nombre, contraseña, plataforma y personaje
    def registrar_usuario_telegram_discord(self, usuario, plataforma, id_ext):
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Insertar en la tabla Usuarios
            cursor.execute("INSERT INTO usuarios (id_usuario, nombre_usuario, password_usuario) VALUES (%s, %s, %s)", 
                           (usuario.id_usuario, usuario.nombre_usuario, usuario.password_usuario))
            
            # Insertar en la tabla Plataformas
            cursor.execute("INSERT INTO plataformas (id_usuario, nombre_plataforma, id_externo_usuario) VALUES (%s, %s, %s)", 
                           (usuario.id_usuario, plataforma, str(id_ext)))
                  
            conn.commit() 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

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

    #-----------------------------------------------------------------------------------------------------------------------------

    #Para evitar que el usuario pueda volver a usar el comando /personaje si ya tiene un personaje elegido
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
            print(f"ÉXITO: Usuario encontrado: {id_interno}")

            
            query2 = "SELECT id_personaje FROM personajes WHERE id_usuario = %s"
            cursor.execute(query2, (id_interno,))
            row2 = cursor.fetchone()

            if row2:
                print(f"ÉXITO: Personaje {row2['id_personaje']} encontrado para usuario {id_interno}")
                
                return {"id_usuario": id_interno, "id_personaje": row2['id_personaje']}
            
            return {"id_usuario": id_interno, "id_personaje": None}       
            
        finally:
            cursor.close()
            conn.close()
    #-----------------------------------------------------------------------------------------------------------------------------