import hashlib

def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    
    hash_intento = hashlib.sha256(password_plana.encode()).hexdigest()
    
    return hash_intento == password_hasheada