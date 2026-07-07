import inspect
from rpg_tasks.core.domain.entidades import Usuario, Plataformas
from rpg_tasks.core.domain.auth_utils import verificar_password
from rpg_tasks.core.domain.clases_personajes import CLASES_DISPONIBLES

#Mensaje de Inicio
class MensajeInicioUseCase:
    def mensaje(self):
        mensaje_inicio = """ Bienvenido a RPG Tasks. 
        ¡Diviértete eligiendo un personaje y subiendo de nivel a medida que completas tareas!
        ¡Los personajes también evolucionan!
        Puedes elegir entre:
            • Guerrero
            • Mago
            • Monje
            • Arquero"""
        return inspect.cleandoc(mensaje_inicio)
    
    def mensaje_registro_telegram(self):
        mensaje = _("En el Menu de abajo tienes un listado de comandos, comienza por crear un usuario o vincular una cuenta y luego elige un personaje")
        return inspect.cleandoc(mensaje)
    
#Simplemente pide las credenciales para crear una cuenta nueva
class CrearCuentaUseCase:
    def nombre_usuario(self):
        mensaje = "Introduce tu nombre de usuario"
        return inspect.cleandoc(mensaje)
    
    def contraseña(self):
        mensaje = "Introduce tu contraseña"
        return inspect.cleandoc(mensaje)
    
    def email(self):
        mensaje = "Introduce tu email"
        return inspect.cleandoc(mensaje)

