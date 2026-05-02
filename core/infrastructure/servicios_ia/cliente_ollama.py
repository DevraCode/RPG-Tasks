import ollama


class OllamaClient:
    def __init__(self, model_name, system_instructions, tools):
        self.model_name = model_name
        self.system_instructions = system_instructions
        self.tools = tools

    def preguntar(self, message:str):
        response = ollama.chat(
                    model=self.model_name,
                    
                               
                    messages=[
                        {'role': 'system', 'content': self.system_instructions},
                        {'role': 'user', 'content': message},
                    ],
                    options={  
                        'temperature': 1.1,
                        'top_p': 0.9
                    }
        )

        respuesta_ia = response['message']['content']
        return respuesta_ia


    def descripcion(self, message: str):
        
        response = ollama.chat(
                    model=self.model_name,
                    
                               
                    messages=[
                        {'role': 'system', 'content': self.system_instructions},
                        {'role': 'user', 'content': message},
                    ],
                    options={  
                        'temperature': 1.1,
                        'top_p': 0.9
                    }
        )
        texto_ia = response['message']['content']
        frases = texto_ia.split('.')
        descripcion_final = ".".join(frases[:7]).strip() + "."
        
        return descripcion_final


