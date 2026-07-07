import os
import hashlib
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

def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    
    hash_intento = hashlib.sha256(password_plana.encode()).hexdigest()
    
    return hash_intento == password_hasheada