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

#Para bots. Utiliza el chat_id del bot para evitar cuentas duplicadas en la BD
def generar_id_usuario_en_plataforma(chat_id):
    id_usuario_en_plataforma = hashlib.sha256(str(chat_id).encode()).hexdigest()[:8]
    return id_usuario_en_plataforma
    
def generar_token_sesion():
    token_generado = secrets.token_hex(16)
    token_sesion = hashlib.sha256(str(token_generado).encode()).hexdigest()[:8]
    return token_sesion


def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    
    hash_intento = hashlib.sha256(password_plana.encode()).hexdigest()
    
    return hash_intento == password_hasheada