from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime
import time
import hashlib


from rpg_tasks.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from rpg_tasks.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from rpg_tasks.infrastructure.repositorios.mysql_plataformas_repository import MySQLPlataformasRepository
from rpg_tasks.infrastructure.repositorios.mysql_tareas_repository import MySQLTareasRepository

from rpg_tasks.core.application.use_cases.usuarios_use_cases import UsuarioUseCase
from rpg_tasks.core.application.use_cases.personajes_use_cases import PersonajeUseCase
from rpg_tasks.core.application.use_cases.plataformas_use_cases import PlataformasUseCase
from rpg_tasks.core.application.use_cases.tareas_use_cases import TareasUseCase
from rpg_tasks.core.application.use_cases.enemigos_use_cases import EnemigosUseCase



from rpg_tasks.infrastructure.servicios_ia.cliente_ollama import OllamaClient


#from .decoradores import usuario_no_existe_o_sesion_cerrada, limite_personajes

from rpg_tasks.infrastructure.dbconfig import db_config

repo_usuarios = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)
repo_plataformas = MySQLPlataformasRepository(db_config)
repo_tareas = MySQLTareasRepository(db_config)

usuarios = UsuarioUseCase(repo_usuarios)
personajes = PersonajeUseCase(repo_personajes, repo_usuarios)
plataformas = PlataformasUseCase(repo_plataformas)
tareas = TareasUseCase(repo_tareas)
enemigos = EnemigosUseCase()

catalogo = personajes.personajes_dic()
lista_personajes = personajes.personajes_list()




from rpg_tasks.infrastructure.servicios_ia.config_ia import SYSTEM_INSTRUCTION




ia = OllamaClient(
    system_instructions=SYSTEM_INSTRUCTION,
)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#Funcion auxiliar que cambia las rutas gif a webm para Telegram exclusivamente
def ruta_webm(clase_personaje):

    datos_personaje = catalogo[clase_personaje]

    imagen = datos_personaje["imagen_personaje"]
    icono_personaje = datos_personaje["icono_personaje"]
    animacion = datos_personaje["animacion_personaje"]

    return imagen, icono_personaje, animacion


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#ELEGIR PERSONAJE

SELECCIONANDO_CLASE, PREGUNTAR_NOMBRE = range(2)


#Primero se enseña la galería de personajes

async def mostrar_personaje(update:Update, context):
    chat_id = update.effective_chat.id

    index = 0 #El índice para manejar los botones
    
    personaje = lista_personajes[index] #lista_personajes[0]
    datos_personaje = catalogo[personaje] #Obtiene los datos del primer personaje de la lista
         
    #Primer teclado para mostrar solamente al primer personaje
    keyboard = [
        [InlineKeyboardButton(datos_personaje["clase"], callback_data="ignore")],
        [
            InlineKeyboardButton("Anterior", callback_data=f"PREV_{index}"),
            InlineKeyboardButton("Siguiente", callback_data=f"NEXT_{index}")
        ],
        [InlineKeyboardButton("Seleccionar", callback_data=f"SELECT_{index}")]
    ]
    
    #Se envía el mensaje a telegram con la imagen del primer personaje y sus botones
    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=datos_personaje["imagen_personaje"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


    return SELECCIONANDO_CLASE #Mantenemos el estado mientras se selecciona al personaje

async def manejador_botones (update:Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "ignore":
        await query.answer()
        return

    await query.answer()


    

    data = query.data.split("_") #Split para que separe el data y obtenga NEXT O PREV con el índice separado ([NEXT, 0] [PREV, 0])
    accion = data[0] #Primera posición de los data obtenidos, o sea, NEXT o PREV
    indice_actual = int(data[1]) #Se convierte a int la segunda posición del data obtenido, que fue 0, que se guardó en la variable index de la función anterior

    #Calculamos los índices
    if accion == "NEXT":
        nuevo_indice = (indice_actual + 1) % len(lista_personajes) #Pasará a NEXT_1, NEXT_2...etc. Y pasa al siguiente personaje
    elif accion == "PREV":
        nuevo_indice = (indice_actual - 1) % len(lista_personajes)#Pasará a PREV_1, PREV_2... Y pasa al anterior personaje
    else:
        nuevo_indice = indice_actual

        personaje_elegido = lista_personajes[nuevo_indice]
        datos_personaje = catalogo[personaje_elegido]

        
        
        context.user_data['imagen_personaje'] = datos_personaje["imagen_personaje_gif"]
        context.user_data['clase_personaje'] = datos_personaje["clase"]
        context.user_data['genero_personaje'] = datos_personaje["genero"]
        context.user_data['icono_personaje'] = datos_personaje["icono_personaje_gif"]
        context.user_data['animacion_personaje'] = datos_personaje["animacion_personaje_gif"]
        context.user_data['nivel_personaje'] = datos_personaje["nivel"]
        
        await query.message.reply_text(f"Has seleccionado la clase {datos_personaje["clase"]}. Ahora, escribe el nombre de tu personaje:")
        
        
        return PREGUNTAR_NOMBRE #Pasa al siguiente estado

    #Borra el Sticker actual y muestra el siguiente, dando la sensación de dinamismo 
    await query.message.delete()


    #Hay que rehacer el teclado para cada personaje
    personaje = lista_personajes[nuevo_indice]
    datos_personaje = catalogo[personaje]
        
    #Creamos el nuevo teclado con el nuevo índice que mostrará al siguiente o al anterior personaje
    nuevo_keyboard = [
        [InlineKeyboardButton(datos_personaje["clase"], callback_data="ignore")],
        [
            InlineKeyboardButton("Anterior", callback_data=f"PREV_{nuevo_indice}"),
            InlineKeyboardButton("Siguiente", callback_data=f"NEXT_{nuevo_indice}")
        ],
        [InlineKeyboardButton("Seleccionar", callback_data=f"SELECT_{nuevo_indice}")]
    ]

    #Se envía el nuevo personaje
    await context.bot.send_sticker(
        chat_id=query.message.chat_id,
        sticker=datos_personaje["imagen_personaje"],
        reply_markup=InlineKeyboardMarkup(nuevo_keyboard)
        )
    
    return SELECCIONANDO_CLASE  #Mientras se selecciona la clase no se cambia de estado
    

#Función que registra al personaje en la base de datos
async def obtener_nombre_personaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_personaje'] = update.message.text

    nombre = context.user_data.get('nombre_personaje')
    imagen = context.user_data.get('imagen_personaje')
    clase = context.user_data.get('clase_personaje')
    genero = context.user_data.get('genero_personaje')
    icono = context.user_data.get('icono_personaje')
    animacion = context.user_data.get('animacion_personaje')
    nivel = context.user_data.get("nivel_personaje")


    prompt_para_ia =(
            f"Escribe una descripción de bardo para este héroe:\n"
            f"Nombre: {nombre}\n"
            f"Clase: {clase}\n"
            f"Género: {genero}\n"
            f"Nivel:{nivel}"
        )
    
    #Mejor poner esto antes de la llamada a la IA, porque tardará en responder
    sticker_carga = "./assets/animaciones/carga/animacion_puntos_suspensivos.webm"
    
    await update.message.reply_text(f"🖋️ Registrando a {nombre} en el gremio, tardará un momento...") 
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=sticker_carga)
    
    
    
    #Llamada a la IA 
    descripcion_epica = ia.descripcion(prompt_para_ia)


    """ Como el id de Telegram no cambia y está asociado al usuario, 
    en este caso da igual buscarlo en la base de datos y hacer una comparación con effective_user.id que poner la variable
    id_generado
    """
    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    

    id_usuario = plataformas.vincular_id_externo_usuario(id_generado) #Se busca el id de usuario interno a través del id_enterno

    
    resultado = personajes.registrar_personaje(
            id_usuario=id_usuario,
            nombre_personaje=nombre,
            genero=genero,
            clase=clase,
            imagen_personaje = imagen,
            icono_personaje= icono,
            animacion_personaje = animacion,
            descripcion_personaje = descripcion_epica

        )
    

    img, icon, anim = ruta_webm(clase.lower()) # Desempaquetar
    

    await update.message.reply_text(f"{resultado}")

    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=img)
    
    await update.message.reply_text(f"{descripcion_epica}")

    return ConversationHandler.END

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#ENTRENAR PERSONAJES

#El usuario elige a un personaje que va a ser entrenado conforme cumple tareas

SELECCIONANDO, ASIGNAR_TAREA, ENTRENAR, COMPLETAR, TEMPORIZADOR = range(5)

#Se muestran los personajes que tiene el usuario en una galeria, igual que para elegir personaje

async def lista_personajes_usuarios(update:Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    id_usuario = plataformas.vincular_id_externo_usuario(id_generado)

    personajes_user = personajes.lista_personajes_usuario(id_usuario) #Devuelve los personajes que tiene el usuario

    index = 0 

    personaje_usuario = personajes_user[index]

    img, icon, anim = ruta_webm(personaje_usuario["clase"].lower())


    keyboard = [
        [InlineKeyboardButton(personaje_usuario["nombre_personaje"], callback_data="ignore")],
        [
            InlineKeyboardButton("Anterior", callback_data=f"PREV_{index}"),
            InlineKeyboardButton("Siguiente", callback_data=f"NEXT_{index}")
        ],
        [InlineKeyboardButton("Entrenar", callback_data=f"SELECT_{index}")]
    ]

    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=icon,
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return SELECCIONANDO



async def manejador_lista_personajes(update:Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "ignore":
        await query.answer()
        return

    await query.answer()

    data = query.data.split("_") 
    accion = data[0] 
    indice_actual = int(data[1])

    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    id_usuario = plataformas.vincular_id_externo_usuario(id_generado)

    personajes_user = personajes.lista_personajes_usuario(id_usuario) #Devuelve los personajes que tiene el usuario

    
    if accion == "NEXT":
        nuevo_indice = (indice_actual + 1) % len(personajes_user) 
    elif accion == "PREV":
        nuevo_indice = (indice_actual - 1) % len(personajes_user)
    else:
        nuevo_indice = indice_actual

        personaje_a_entrenar = personajes_user[nuevo_indice]
        
        context.user_data["id_personaje"] = personaje_a_entrenar["id_personaje"] #Guardamos el id del personaje

        return await menu_tareas(update, context) #Muestra el listado de tareas

    
    await query.message.delete()
    
    nuevo_personaje = personajes_user[nuevo_indice]
    img, icon, anim = ruta_webm(nuevo_personaje["clase"].lower())
    
    nuevo_keyboard = [
        [InlineKeyboardButton(nuevo_personaje["nombre_personaje"], callback_data="ignore")],
        [
            InlineKeyboardButton("Anterior", callback_data=f"PREV_{nuevo_indice}"),
            InlineKeyboardButton("Siguiente", callback_data=f"NEXT_{nuevo_indice}")
        ],
        [InlineKeyboardButton("Seleccionar", callback_data=f"SELECT_{nuevo_indice}")]
    ]

    
    await context.bot.send_sticker(
        chat_id=query.message.chat_id,
        sticker=icon,
        reply_markup=InlineKeyboardMarkup(nuevo_keyboard)
        )
    
    return SELECCIONANDO  


async def menu_tareas(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()


    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    id_usuario = plataformas.vincular_id_externo_usuario(id_generado)

    lista_tareas = tareas.lista_tareas_usuario(id_usuario)

    keyboard = []

    for tarea in lista_tareas:
        boton = [InlineKeyboardButton(
            text=f"{tarea['nombre_tarea'].capitalize()}", 
            callback_data=f"{tarea["id_tarea"]}" 
        )]
        keyboard.append(boton)
        

    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="Selecciona una Quest del tablón de Misiones:",
    reply_markup=InlineKeyboardMarkup(keyboard),
    parse_mode="Markdown"
    )

    
    return ASIGNAR_TAREA

  
async def asignar_tarea(update:Update, context: CallbackContext):
    query = update.callback_query
    id_tarea = query.data

    context.user_data["id_tarea"] = id_tarea #Guardamos el id de la tarea

    tarea = tareas.buscar_tarea_por_id(id_tarea)

    nombre_tarea = tarea["nombre_tarea"]

    id_personaje = context.user_data.get("id_personaje") #Recuperamos el id del personaje
    personaje = personajes.buscar_personaje_por_id(id_personaje) # Y lo buscamos en la BD

    nombre_personaje = personaje["nombre_personaje"]

    await query.edit_message_text(f"Has elegido a {nombre_personaje} con la Quest {nombre_tarea.capitalize()}")

    return await teclado_temporizador(update, context) #Llama a la función teclado_temporizador


#Solo muestra las opciones
async def teclado_temporizador(update:Update, context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text="Si", callback_data="SI")],
        [InlineKeyboardButton(text="No", callback_data="NO")],
    ]
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="¿Quieres establecer un temporizador?",
    reply_markup=InlineKeyboardMarkup(keyboard),
    parse_mode="Markdown"
    )

    return ENTRENAR

#Solo muestra la animacion de batalla
async def batalla(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    id_personaje = context.user_data.get("id_personaje") #Recuperamos el id del personaje
    personaje = personajes.buscar_personaje_por_id(id_personaje) # Y lo buscamos en la BD

    id_tarea = context.user_data.get("id_tarea") #Recuperamos el id de la tarea

    tareas.vincular_personaje_con_tarea(id_personaje, id_tarea) #Vinculamos la tarea al personaje en la BD

    img, icon, anim = ruta_webm(personaje["clase"].lower())

    boss = enemigos.enemigo_aleatorio_webm()

    await context.bot.send_sticker(
    chat_id=query.message.chat_id,
    sticker=boss
    )

    await context.bot.send_sticker(
    chat_id=query.message.chat_id,
    sticker=anim
    )

#Funcion que muestra el teclado de los minutos
async def teclado_minutos(update:Update, context:CallbackContext):
    valor_inicial = 0
    
    keyboard = [
        [InlineKeyboardButton(text=str(valor_inicial), callback_data="ignore")],
        [
            InlineKeyboardButton(text="-", callback_data=f"CAMBIAR_{max(0, valor_inicial - 1)}"),
            InlineKeyboardButton(text="+", callback_data=f"CAMBIAR_{valor_inicial + 1}")
            
        ],
        [InlineKeyboardButton(text="Confirmar", callback_data=f"CONFIRMAR_{valor_inicial}")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Selecciona los minutos:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def manejador_minutos(update:Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    accion = data[0]
    
    if accion == "ignore":
        return

    valor_actual = int(data[1])

    if accion == "CAMBIAR":
        
        nuevo_valor = valor_actual
        
        keyboard = [
            [InlineKeyboardButton(text=f"{nuevo_valor} min", callback_data="ignore")],
            [
                InlineKeyboardButton(text="-", callback_data=f"CAMBIAR_{max(0, nuevo_valor - 1)}"),
                InlineKeyboardButton(text="+", callback_data=f"CAMBIAR_{nuevo_valor + 1}")
                
            ],
            [InlineKeyboardButton(text="Confirmar", callback_data=f"CONFIRMAR_{nuevo_valor}")]
        ]
        
        
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif accion == "CONFIRMAR":
        await query.edit_message_text(text=f"La tarea se completará automáticamente en {valor_actual} minutos.")
        minutos = valor_actual
        segundos = minutos * 60
        chat_id = update.effective_chat.id

        context.job_queue.run_once(
            callback=aviso_finalizacion, 
            when=segundos, 
            chat_id=chat_id,
            data=context.user_data.get("id_personaje") 
        )

        boton_completar_tarea = [
            [InlineKeyboardButton(text="Terminar", callback_data="TERMINAR")]
        ]

        await context.bot.send_message(chat_id=update.effective_chat.id, text = "¡Que empiece la batalla!")
        await batalla(update, context)
        await query.message.reply_text(text = "Quest en proceso...", reply_markup=InlineKeyboardMarkup(boton_completar_tarea))

        

        return COMPLETAR
        


async def entrenar(update:Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == "NO":

        boton_completar_tarea = [
            [InlineKeyboardButton(text="Terminar", callback_data="TERMINAR")]
        ]

        await query.delete_message()
        await context.bot.send_message(chat_id=update.effective_chat.id, text = "¡Ha aparecido un enemigo! ¡Completa la Quest para vencerlo!")
        await batalla(update, context)
        await query.message.reply_text(text = "Completando la Quest...", reply_markup=InlineKeyboardMarkup(boton_completar_tarea))

        #Guardamos el tiempo al que se inicia la tarea
        tiempo_inicio = datetime.now()
        context.user_data["tiempo_inicio"] = tiempo_inicio

        return COMPLETAR
        
    else:

        await query.delete_message() 
        await teclado_minutos(update, context)   
        return TEMPORIZADOR


async def completar_tarea(update:Update, context:CallbackContext):
    query = update.callback_query
    data = query.data

    if data == "TERMINAR":
        id_tarea = context.user_data.get("id_tarea") #Recuperamos el id de la tarea
        id_personaje = context.user_data.get("id_personaje") #Recuperamos el id del personaje

        #Llamar a funcion de completar tarea y subir exp
        tareas.completar_tarea(id_tarea) #Completar tarea

        #Buscamos al personaje en la BD para saber su exp
        personaje = personajes.buscar_personaje_por_id(id_personaje)
        exp_personaje = int(personaje["exp"])

        #Aplicamos la lógica de subida de exp
        nueva_exp = tareas.experiencia_tarea_completada() #+150 exp por tarea completada
        subida_exp = personajes.subir_exp(exp_personaje,nueva_exp)

        #Ahora llamariamos a subida de nivel si ha llegado al límite de exp del personaje
        #Primero buscamos la exp actual del personaje (ya la tenemos)
        #Lo comparamos con el limite de exp definido en la lógica de personajes
        #Si lo supera se llamará a la función subida de nivel que habrá que definir ahora
        #Y se sube el resultado  a la BD

        

        #Poner un temporizador interno que empiece a partir del "¡Ha aparecido un enemigo!" que sume el tiempo que se tarda en darle al botón terminar
        tiempo_inicio = context.user_data.get("tiempo_inicio") #Recuperamos el tiempo en el que empezó la tarea
        tiempo_fin = datetime.now()
        tiempo = tareas.temporizador_interno(tiempo_inicio, tiempo_fin)

        segundos_enteros = int(tiempo.total_seconds())
        horas, resto = divmod(segundos_enteros, 3600)
        minutos, segundos = divmod(resto, 60)

        tiempo_transcurrido = f"{horas} Horas, {minutos} minutos y {segundos} segundos"

        await context.bot.send_message(chat_id = update.effective_chat.id, text = f"¡Quest Completada! Has conseguido +{nueva_exp} EXP y Has tardado {tiempo_transcurrido} en completar la tarea")

        #Cuanto menos tiempo se tarde, más exp (hacer funcion que de bonos de exp cada x segundos a partir de cierto tiempo hasta cierto tiempo, se reduce la exp a medida que pasa el tiempo)


        #Se sube la exp a la bd
        personajes.subir_exp_bd(subida_exp,id_personaje)


        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "Aun no has terminado la Quest")
        return COMPLETAR
    

async def aviso_finalizacion(context: CallbackContext):
    job = context.job
    id_personaje = job.data
    
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text=f"¡El entrenamiento ha terminado! Tu personaje ha ganado experiencia."
    )