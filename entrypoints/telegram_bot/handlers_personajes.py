from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext
import hashlib

from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import ObtenerCatalogoUseCase, VincularIdExternoUseCase, RegistrarPersonajeUseCase

from .decoradores import usuario_no_registrado, personaje_elegido

from .dbconfig import db_config

repo = MySQLUsuarioRepository(db_config)
use_case = ObtenerCatalogoUseCase()
vincular_id_externo_use_case = VincularIdExternoUseCase(repo)
registrar_personaje_use_case = RegistrarPersonajeUseCase(repo)




catalogo = use_case.personajes_dic()
lista_personajes = use_case.personajes_list()


SELECCIONANDO_CLASE, PREGUNTAR_NOMBRE = range(2)


#PRIMERO SE ENSEÑA EL CATÁLOGO DE PERSONAJES
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
        context.user_data['imagen_personaje'] = datos_personaje["imagen_personaje_gif"] #Para la base de datos
        context.user_data['clase_personaje'] = datos_personaje["clase"]
        context.user_data['genero_personaje'] = datos_personaje["genero"]
        
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
    
    return SELECCIONANDO_CLASE #Mientras se selecciona la clase no se cambia de estado
    
async def obtener_nombre_personaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_personaje'] = update.message.text

    nombre = context.user_data.get('nombre_personaje')
    imagen = context.user_data.get('imagen_personaje')
    clase = context.user_data.get('clase_personaje')
    genero = context.user_data.get('genero_personaje')

    print(f"Usuario escribió: {nombre}")

    """ Como el id de Telegram no cambia y está asociado al usuario, 
    en este caso da igual buscarlo en la base de datos y hacer una comparación con effective_user.id que poner la variable
    id_generado
    """
    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    print(f"DEBUG 1 - Hash Telegram: {id_generado}")

    id_usuario = vincular_id_externo_use_case.vincular_id_externo_usuario(id_generado) #Se busca el id de usuario interno a través del id_enterno

    print(f"DEBUG 2 - ID Usuario recuperado: {id_usuario}")
    resultado = registrar_personaje_use_case.ejecutar(
            id_usuario=id_usuario,
            nombre_personaje=nombre,
            genero=genero,
            clase=clase,
            imagen_personaje = imagen
        )

    await update.message.reply_text(f"{resultado}")

    return ConversationHandler.END

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Muestra los personajes que tiene el usuario

#Ahora solo esta comprobando que envia bien el icono
async def lista_personajes_usuarios(update:Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    personaje = lista_personajes[0]
    datos_personaje = catalogo[personaje]


    nuevo_keyboard = [
        [InlineKeyboardButton(datos_personaje["clase"], callback_data="ignore")]
        
    ]

    await context.bot.send_sticker(
        chat_id=chat_id,
        sticker=datos_personaje["icon_personaje"],
        reply_markup=InlineKeyboardMarkup(nuevo_keyboard)
        )


