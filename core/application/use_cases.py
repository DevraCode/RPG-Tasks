# core/application/use_cases.py
import uuid
import hashlib
import inspect
from core.domain.models import Usuario, Personaje
from core.domain.auth_utils import verificar_password


from core.domain.clases_personajes import CLASES_DISPONIBLES

#Mensaje de Inicio
class MensajeInicioUseCase:
    def mensaje(self):
        mensaje_inicio = """ Bienvenido a RPG Tasks 
        Crea tu cuenta o inicia sesión y ya podrás empezar a usar la aplicación. 
        ¡Diviértete eligiendo un personaje y subiendo de nivel a medida que completas tareas!
        ¡Los personajes también evolucionan!
        Puedes elegir entre:
            • Guerrero
            • Mago
            • Monje
            • Arquero"""
        return inspect.cleandoc(mensaje_inicio)


#Simplemente pide las credenciales para crear una cuenta nueva
class CrearCuentaUseCase:
    def nombre_usuario(self):
        mensaje = "Introduce tu nombre de usuario"
        return inspect.cleandoc(mensaje)
    def contraseña(self):
        mensaje = "Introduce una contraseña"
        return inspect.cleandoc(mensaje)


#Comprueba que el nombre de usuario ya exista en la base de datos
class UsuarioExiste:
    def __init__(self, repo):
        self.repo = repo

    def usuario_existe(self, nombre_usuario: str):
        usuario = self.repo.buscar_usuario_en_bd(nombre_usuario)
        if usuario:
            mensaje = "Ese usuario ya existe"
            return mensaje



#Registra a un usuario nuevo
class RegistroNuevoJugadorUseCase:
    def __init__(self, repo):
        self.repo = repo


    def ejecutar(self, id_externo: str, plataforma: str, nombre_usuario: str, password_usuario: str):
        # Comprobar que el usuario existe en la base de datos (se comprueba por nombre)
        #existente = self.repo.buscar_por_id_externo(id_externo, plataforma)
        usuario = self.repo.buscar_usuario_en_bd(nombre_usuario)
        if usuario:
            return f"El nombre {usuario.nombre_usuario.capitalize()} ya existe"

        #El id del usuario sera una mezcla del id de la plataforma desde donde se conecte y su nombre de usuario
        id_externo_bytes = f"{id_externo}{nombre_usuario}".encode()
        nuevo_id = hashlib.sha256(id_externo_bytes).hexdigest()[:8]



        nuevo_usuario = Usuario(id_usuario=nuevo_id, nombre_usuario=nombre_usuario, password_usuario=password_usuario)
        nuevo_personaje = Personaje(id_usuario=nuevo_id)

        # Guardamos todo en MySQL
        self.repo.registrar_usuario_completo(nuevo_usuario, plataforma, id_externo, nuevo_personaje)
        
        return f"¡Cuenta creada! Tu ID universal es {nuevo_id}. ¡A la aventura!"



class ObtenerSaludoUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, id_externo: str, plataforma: str) -> str:
        # 1. Buscamos al usuario en la DB a través del repositorio
        usuario_existente = self.repo.buscar_por_id_externo(id_externo, plataforma)

        if not usuario_existente:
            return "¡Hola viajero desconocido! Crea una cuenta para empezar a usar la aplicación"

        # 2. Si existe, podríamos incluso buscar su personaje para un saludo épico
        # (Por ahora usemos solo el nombre que recuperamos de la DB)
        return f"¡Saludos, {usuario_existente.nombre_usuario}! Es un honor verte de nuevo."
    

class ObtenerCatalogoUseCase:
    def ejecutar(self):
        
        return CLASES_DISPONIBLES