# core/application/use_cases.py
import uuid
import hashlib
import inspect
from core.domain.models import Usuario, Plataformas
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
    
    def email(self):
        mensaje = "Introduce tu email"
        return inspect.cleandoc(mensaje)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------    

class UsuarioUsecase:
    def __init__(self, repo):
        self.repo = repo

    def registrar_usuario(self, nombre_usuario: str, password_usuario: str, email_usuario: str, rango: str, tipo_usuario:int, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str):
        nuevo_usuario = Usuario(
            id_usuario = None,
            nombre_usuario = nombre_usuario,
            password_usuario = password_usuario,
            email_usuario = email_usuario,
            rango = rango,
            tipo_usuario = tipo_usuario

        )
        registro = self.repo.registrar_usuario(nuevo_usuario, id_plataforma, nombre_plataforma, id_externo_usuario)
        return registro
    
    def id_usuario_existe(self, id_usuario: int):
        usuario = self.repo.buscar_por_id_usuario(id_usuario)
        
        return usuario
    
    def nombre_usuario_existe(self, nombre_usuario: str):
        usuario = self.repo.buscar_usuario_en_bd(nombre_usuario)
        if usuario:
            mensaje = "Ese usuario ya existe"
            return mensaje
        
    def id_externo(self, id_externo_usuario: str):
        usuario = self.repo.buscar_usuario_en_bd(id_externo_usuario)
        return usuario
    
    def buscar_usuario_por_nombre(self, nombre_usuario: str):
        resultado = self.repo.buscar_usuario_por_nombre(nombre_usuario)
        return resultado
    
    def buscar_id_externo_usuario(self, id_externo, nombre_plataforma):
        self.repo.buscar_por_id_externo(id_externo, nombre_plataforma)

    def comprobar_usuario(self, nombre_usuario:str, password_usuario:str):
        resultado = self.repo.comprobar_usuario_contraseña(nombre_usuario, password_usuario)
        return resultado

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------   

class PersonajeUseCase:
    def __init__(self, repo):
        self.repo = repo

    def registrar_personaje(self, id_usuario, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje):
        usuario = self.repo.buscar_por_id_usuario(id_usuario)
        if usuario is None:
            
            print(f"LOG: No se pudo registrar personaje. El usuario {id_usuario} no existe.")
            return "Error: El usuario no existe en la base de datos."
        
        self.repo.registrar_personaje_elegido(
            id_usuario, 
            nombre_personaje, 
            genero, 
            clase, 
            imagen_personaje,
            icono_personaje,
            animacion_personaje
        )
        return "¡Personaje elegido!"
    
    def personajes_dic(self):
        return CLASES_DISPONIBLES
    
    def personajes_list(self) -> list:
        claves = list(CLASES_DISPONIBLES.keys())
        return claves
    
    def limite_personajes_usuario(self, id_usuario):
        limite = self.repo.limite_personajes_de_usuario(id_usuario)
        
        return limite
    
    def lista_personajes_usuario(self,id_usuario):
        lista_personajes = self.repo.lista_personajes_usuario(id_usuario)

        return lista_personajes
    
    def vincular_id_personaje_con_usuario(self, id_externo):
        resultado = self.repo.vincular_id_personaje_con_usuario(id_externo)

        return resultado

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

class PlataformasUseCase:
    def __init__(self, repo):
        self.repo = repo

    def usuario_activo(self, id_usuario):

        sesion = self.repo.obtener_estado_sesion(id_usuario)
        
        return sesion
    
    def vincular_id_externo_usuario(self, id_externo):
        resultado = self.repo.vincular_id_externo_con_interno(id_externo)

        return resultado
    
    

    def vincular_plataforma(self, id_plataforma: int, nombre_plataforma: str, id_externo_usuario: str, id_usuario: int):
        nueva_plataforma = Plataformas(
            id_plataforma = id_plataforma,
            nombre_plataforma = nombre_plataforma
        )

        vinculacion = self.repo.vincular_plataforma(nueva_plataforma, id_usuario, id_externo_usuario)
        return vinculacion
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------