import google.generativeai as genai
from core.infrastructure.servicios_ia.gemini_tools import gemini_tools

from core.infrastructure.dbconfig import db_config

mis_herramientas = gemini_tools(db_config)

class GeminiService:
    def __init__(self, api_key, model_name, tools=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=mis_herramientas
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def ask(self, message):
        response = self.chat.send_message(message)
        return response.text