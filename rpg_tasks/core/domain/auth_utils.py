import os
import hashlib
import secrets
import uuid
from hashids import Hashids


secret_word = os.getenv("SECRET_WORD", "DEFAULT_SECRET_WORD")

hashids = Hashids(salt=secret_word, min_length=8)

def codificar_id_usuario(id_usuario):
    id_codificada = hashids.encode(id_usuario)
    return id_codificada

def decodificar_id_usuario(id_codificada):
    id_decodificada = hashids.decode(id_codificada)
    if id_decodificada:
        return id_decodificada[0]
    else:
        return None
    
def generar_id_externo():
    id_externo = str(uuid.uuid4())
    return id_externo

#Genera un id para el usuario en una plataforma segun el parametro que le pasemos. En este caso, el id del dispositvo o del chat, que es un id único
def generar_id_usuario_en_plataforma(parametro):
    id_usuario_en_plataforma = hashlib.sha256(str(parametro).encode()).hexdigest()[:8]
    return id_usuario_en_plataforma
    
def generar_token_sesion():
    token_generado = secrets.token_hex(16)
    return token_generado

