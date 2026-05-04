import ollama
from .ollama_tools import OllamaTools

class OllamaClient:
    def __init__(self, system_instructions, tools):
        self.model_name = "hermes3" 
        self.system_instructions = system_instructions
        self.ollama_tools = OllamaTools()
        self.lista_tools = list(self.ollama_tools.ollama_tools().values())
        self.tools = self.lista_tools

    def preguntar(self, message: str):
        funciones_mapa = self.ollama_tools.ollama_tools()
        
        mensajes = [
            {'role': 'system', 'content': self.system_instructions}, 
            {'role': 'user', 'content': message},
        ]

        response = ollama.chat(
            model=self.model_name,
            messages=mensajes,
            tools=self.tools,
        )

        while response['message'].get('tool_calls'):
            
            mensajes.append(response['message'])

            for tool in response['message']['tool_calls']:
                nombre_f = tool['function']['name']
                argumentos = tool['function']['arguments']
                
                if nombre_f in funciones_mapa:
                    print(f"DEBUG: Ejecutando {nombre_f}({argumentos})")
                    resultado = funciones_mapa[nombre_f](**argumentos)
                    
                    mensajes.append({
                        'role': 'tool',
                        'content': str(resultado),
                        'name': nombre_f
                    })
            
            response = ollama.chat(
                model=self.model_name,
                messages=mensajes
            )

        return response['message']['content']


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


