# core/application/use_cases.py
import uuid
import inspect
from core.domain.models import Usuario, Personaje


class MensajeInicioUseCase:
    def mensaje(self):
        mensaje_inicio = """
        Bienvenido a RPG Tasks 
        Registrate en el sistema a través de:
            • El Formulario Web (próximamente)
            • En la App de Android (próximamente) 
            • Usando el comando /registro en Telegram 
            • Usando el comando !registro en Discord
        """
        return inspect.cleandoc(mensaje_inicio)
    
    def segundo_mensaje(self):
        segundo_mensaje = """Crea tu Nombre de Usuario y tu Contraseña y ya podrás empezar a usar la aplicación. 
        ¡Diviértete eligiendo un personaje y subiendo de nivel a medida que completas tareas!
        ¡Los personajes también evolucionan!
        Puedes elegir entre:
            • Guerrero
            • Mago
            • Monje
            • Arquero"""
        return inspect.cleandoc(segundo_mensaje)

class RegistroNuevoJugadorUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, id_externo: str, plataforma: str, nombre_usuario: str, password_usuario: str):
        # 1. ¿Ya existe?
        existente = self.repo.buscar_por_id_externo(id_externo, plataforma)
        if existente:
            return f"¡Bienvenido de nuevo, {existente.nombre_usuario}!"

        # 2. Si no existe, creamos la identidad maestra (UUID)
        nuevo_id = str(uuid.uuid4())[:8]

        nuevo_usuario = Usuario(id_usuario=nuevo_id, nombre_usuario=nombre_usuario, password_usuario=password_usuario)
        nuevo_personaje = Personaje(id_usuario=nuevo_id)

        # 3. Guardamos todo en MySQL
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