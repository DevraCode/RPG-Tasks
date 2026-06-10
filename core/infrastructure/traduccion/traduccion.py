from deep_translator import GoogleTranslator as RealTimeGoogle

IDIOMAS_USUARIOS = {}

def translate(key: str, lang: str) -> str:
        if lang.startswith('es'):
            return key
            
        try:
            return RealTimeGoogle(source='es', target=lang).translate(key)
        
        except Exception as e:
            print(f"Error en la API de traducción: {e}")
            return key  