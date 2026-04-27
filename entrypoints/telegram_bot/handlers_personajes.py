from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext
import hashlib

from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases import ObtenerCatalogoUseCase, VincularIdExternoUseCase, RegistrarPersonajeUseCase, ListaPersonajesUsuarioUseCase

from .decoradores import usuario_no_registrado, personaje_elegido

from .dbconfig import db_config

repo = MySQLUsuarioRepository(db_config)
use_case = ObtenerCatalogoUseCase()
vincular_id_externo_use_case = VincularIdExternoUseCase(repo)
registrar_personaje_use_case = RegistrarPersonajeUseCase(repo)
lista_personajes_usuarios_use_case = ListaPersonajesUsuarioUseCase(repo)


catalogo = use_case.personajes_dic()
lista_personajes = use_case.personajes_list()

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
@usuario_no_registrado #Comprobar que el usuario se ha registrado primero o que esté o no baneado
@personaje_elegido #Comprobar que el usuario haya elegido o no personaje
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
        
        print(f"Usuario eligió a: {personaje_elegido}")
        context.user_data['imagen_personaje'] = datos_personaje["imagen_personaje_gif"]
        context.user_data['clase_personaje'] = datos_personaje["clase"]
        context.user_data['genero_personaje'] = datos_personaje["genero"]
        context.user_data['icono_personaje'] = datos_personaje["icono_personaje_gif"]
        context.user_data['animacion_personaje'] = datos_personaje["animacion_personaje_gif"]
        
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


    """ Como el id de Telegram no cambia y está asociado al usuario, 
    en este caso da igual buscarlo en la base de datos y hacer una comparación con effective_user.id que poner la variable
    id_generado
    """
    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    

    id_usuario = vincular_id_externo_use_case.vincular_id_externo_usuario(id_generado) #Se busca el id de usuario interno a través del id_enterno

    
    resultado = registrar_personaje_use_case.ejecutar(
            id_usuario=id_usuario,
            nombre_personaje=nombre,
            genero=genero,
            clase=clase,
            imagen_personaje = imagen,
            icono_personaje= icono,
            animacion_personaje = animacion

        )

    await update.message.reply_text(f"{resultado}")

    return ConversationHandler.END

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#ENTRENAR PERSONAJES

#El usuario elige a un personaje que va a ser entrenado conforme cumple tareas

SELECCIONANDO, ASIGNAR_TAREA = range(2)

#Se muestran los personajes que tiene el usuario en una galeria, igual que para elegir personaje
async def lista_personajes_usuarios(update:Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    id_usuario = vincular_id_externo_use_case.vincular_id_externo_usuario(id_generado)

    personajes = lista_personajes_usuarios_use_case.lista_personajes_usuario(id_usuario) #Devuelve los personajes que tiene el usuario

    index = 0 

    personaje_usuario = personajes[index]

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
    id_usuario = vincular_id_externo_use_case.vincular_id_externo_usuario(id_generado)

    personajes = lista_personajes_usuarios_use_case.lista_personajes_usuario(id_usuario) #Devuelve los personajes que tiene el usuario

    
    if accion == "NEXT":
        nuevo_indice = (indice_actual + 1) % len(personajes) 
    elif accion == "PREV":
        nuevo_indice = (indice_actual - 1) % len(personajes)
    else:
        nuevo_indice = indice_actual

        personaje_a_entrenar = personajes[nuevo_indice]
        
        print(f"Usuario eligió a: {personaje_a_entrenar["nombre_personaje"]}")

        await query.message.reply_text(f"Has seleccionado a {personaje_a_entrenar["nombre_personaje"]}. Elige la tarea con la que quieres entrenarle")
        
        
        return ASIGNAR_TAREA #Pasa al siguiente estado

    
    await query.message.delete()


    
    nuevo_personaje = personajes[nuevo_indice]
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


async def asignar_tarea(update:Update, context: ContextTypes.DEFAULT_TYPE):

    #Aquí se mostraria una lista de tareas que el usuario ha registrado previamente, se elige la tarea y se altera la tabla tareas con el id del personaje para luego hacer la lógica de subida de exp, etc
    await update.message.reply_text(f"wiiiiiii") #Mensaje de prueba