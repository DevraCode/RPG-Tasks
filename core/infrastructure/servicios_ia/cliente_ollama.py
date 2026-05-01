import ollama 

class OllamaClient:
    def __init__(self, model_name, system_instructions):
        self.model_name = model_name,
        self.system_instructions = system_instructions

    def ask(self, message: str):
        
        response = ollama.chat(model=self.model_name, messages=[
            {'role': 'system', 'content': self.system_instruction},
            {'role': 'user', 'content': message},
        ])
        return response['message']['content']
