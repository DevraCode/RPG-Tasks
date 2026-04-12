from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext




from core.application.use_cases import ObtenerCatalogoUseCase

use_case = ObtenerCatalogoUseCase() 
catalogo = use_case.personajes_dic()
lista_personajes = use_case.personajes_list()


async def mostrar_personaje(update:Update, context):
    chat_id = update.effective_chat.id

    index = 0 #El índice para manejar los botones
    
    personaje = lista_personajes[index] #lista_personajes[0]
    datos_personaje = catalogo[personaje] #Obtiene los datos del primer personaje de la lista
         
    #Primer teclado para mostrar solamente al primer personaje
    keyboard = [
        [InlineKeyboardButton(datos_personaje["id"], callback_data="ignore")],
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
        sticker=datos_personaje["imagen"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

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
        #LLAMAR AQUI A FUNCION PARA GUARDAR EN LA DB
        print(f"Usuario eligió a: {personaje_elegido}")
        return

    #Borra el Sticker actual y muestra el siguiente, dando la sensación de dinamismo 
    await query.message.delete()


    #Hay que rehacer el teclado para cada personaje
    personaje = lista_personajes[nuevo_indice]
    datos_personaje = catalogo[personaje]
        
    #Creamos el nuevo teclado con el nuevo índice que mostrará al siguiente o al anterior personaje
    nuevo_keyboard = [
        [InlineKeyboardButton(datos_personaje["id"], callback_data="ignore")],
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
        sticker=datos_personaje["imagen"],
        reply_markup=InlineKeyboardMarkup(nuevo_keyboard)
        )
