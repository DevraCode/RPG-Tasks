# core/application/use_cases.py
import uuid
from core.domain.models import Usuario, Personaje

class RegistroNuevoJugadorUseCase:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, id_externo: str, plataforma: str, nombre_sugerido: str):
        # 1. ¿Ya existe?
        existente = self.repo.buscar_por_id_externo(id_externo, plataforma)
        if existente:
            return f"¡Bienvenido de nuevo, {existente.nombre_jugador}!"

        # 2. Si no existe, creamos la identidad maestra (UUID)
        nuevo_id = str(uuid.uuid4())
        nuevo_usuario = Usuario(id_interno=nuevo_id, nombre_jugador=nombre_sugerido)
        nuevo_personaje = Personaje(id_interno=nuevo_id, clase="Guerrero") # Clase por defecto

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
            return "¡Hola viajero desconocido! Usa /start para registrarte."

        # 2. Si existe, podríamos incluso buscar su personaje para un saludo épico
        # (Por ahora usemos solo el nombre que recuperamos de la DB)
        return f"¡Saludos, {usuario_existente.nombre_jugador}! Es un honor verte de nuevo."