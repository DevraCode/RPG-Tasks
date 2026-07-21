import ollama
from rpg_tasks.core.application.output_ports.ollama_output_port import OllamaOutputPort

class OllamaAdapter(OllamaOutputPort):
    def __init__(self, system_instructions):
        self.model_name = "hermes3" 
        self.system_instructions = system_instructions

    def generar_descripcion(self, message: str):
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


