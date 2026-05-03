import ollama


class OllamaClient:
    def __init__(self, system_instructions, tools):
        self.model_name = "llama3.1-libre" 
        self.system_instructions = system_instructions
        self.tools = tools

    def preguntar(self, message: str):
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': self.system_instructions}, 
                {'role': 'user', 'content': message},
            ],
            tools=self.tools,
        )

         
            
        if hasattr(response.message, 'tool_calls') and response.message.tool_calls:
            llamadas_procesadas = []
            
            for tool in response.message.tool_calls:
                
                llamadas_procesadas.append({
                    'function': {
                        'name': tool.function.name,
                        'arguments': tool.function.arguments
                    }
                })
            
            
            return llamadas_procesadas

        
        return response.message.content




       



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


