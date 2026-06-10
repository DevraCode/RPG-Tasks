import inspect
from core.domain.entidades import Usuario, Plataformas
from core.domain.auth_utils import verificar_password
from core.domain.clases_personajes import CLASES_DISPONIBLES

#Mensaje de Inicio
class MensajeInicioUseCase:
    def mensaje(self):
        mensaje_inicio = _(""" Bienvenido a RPG Tasks 
        Crea tu cuenta o inicia sesión y ya podrás empezar a usar la aplicación. 
        ¡Diviértete eligiendo un personaje y subiendo de nivel a medida que completas tareas!
        ¡Los personajes también evolucionan!
        Puedes elegir entre:
            • Guerrero
            • Mago
            • Monje
            • Arquero""")
        return inspect.cleandoc(mensaje_inicio)
    
    def mensaje_registro_telegram(self):
        mensaje = _("Utiliza el comando /registro para crear una cuenta. Si ya tienes cuenta, utiliza el comando /vincular para iniciar sesión")
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

