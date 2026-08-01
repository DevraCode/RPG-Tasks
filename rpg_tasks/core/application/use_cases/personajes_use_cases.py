import hashlib
from rpg_tasks.core.domain.clases_personajes import CLASES_DISPONIBLES
from rpg_tasks.core.domain.logica_personajes import LogicaPersonajes
from rpg_tasks.core.application.output_ports.ollama_output_port import OllamaOutputPort


logica_personajes = LogicaPersonajes()



class PersonajeUseCase:

    def __init__(self, repo_personajes, repo_usuarios, ollama: OllamaOutputPort):
        self.repo_personajes = repo_personajes  # Para guardar el personaje
        self.repo_usuarios = repo_usuarios
        self.ollama = ollama

    def registrar_personaje(self, nombre_personaje, genero, clase, imagen_personaje, icono_personaje, animacion_personaje, descripcion_personaje, id_usuario_en_plataforma):
        
        #Buscamos primero al usuario
        id_usuario_en_plataforma_hasheado = hashlib.sha256(id_usuario_en_plataforma.encode('utf-8')).hexdigest()[:8]
        usuario = self.repo_usuarios.buscar_usuario_por_id_plataforma(id_usuario_en_plataforma_hasheado)
        
        if usuario is None: 
            return "Error: El usuario no existe en la base de datos."
        
        id_usuario = usuario.id_usuario

        prompt_para_ia =(
            f"Escribe una descripción de bardo para este héroe:\n"
            f"Nombre: {nombre_personaje}\n"
            f"Clase: {clase}\n"
            f"Género: {genero}\n"
        )

        descripcion_personaje = self.ollama.generar_descripcion(prompt_para_ia)
        
        self.repo_personajes.registrar_personaje_elegido(
            id_usuario, 
            nombre_personaje, 
            genero, 
            clase, 
            imagen_personaje,
            icono_personaje,
            animacion_personaje,
            descripcion_personaje
        )
        return descripcion_personaje #Devolvemos la descripcion del personaje para el endpoint
    

    
    

    def buscar_personaje_por_id(self, id_personaje):
        personaje = self.repo_personajes.buscar_personaje_por_id(id_personaje)

        return personaje
    
    
    
    def personajes_dic(self):
        return CLASES_DISPONIBLES
    
    def personajes_list(self) -> list:
        claves = list(CLASES_DISPONIBLES.keys())
        return claves
    
    def limite_personajes_usuario(self, id_usuario):
        limite = self.repo_personajes.limite_personajes_de_usuario(id_usuario)
        
        return limite
    


    def lista_personajes_usuario(self,id_usuario):

        lista_personajes = self.repo_personajes.lista_personajes_usuario(id_usuario)

        return lista_personajes
    



    def vincular_id_personaje_con_usuario(self, id_externo):
        resultado = self.repo_personajes.vincular_id_personaje_con_usuario(id_externo)

        return resultado
    
    def subir_exp(self,exp_actual, nueva_exp):
        return logica_personajes.subir_exp(exp_actual, nueva_exp)

    def subir_exp_bd(self,exp,id_personaje):
        self.repo_personajes.subida_experiencia(exp,id_personaje)


    