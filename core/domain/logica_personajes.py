
class LogicaPersonajes:

    def __init__(self):
        pass

    def limite_exp(self,nivel_actual):
        nuevo_limite = nivel_actual * 1000
        return nuevo_limite

    def subir_exp(self, exp_actual, exp_adquirida):
         nueva_exp = exp_actual + exp_adquirida

         return nueva_exp
    
    def subir_nivel(self, exp_actual, nivel_actual):
        nuevo_nivel = nivel_actual
        nueva_exp = exp_actual
        limite = self.limite_exp(nivel_actual) 

        if exp_actual >= limite: 
            nuevo_nivel += 1    
            nueva_exp = 0       
            
            return nueva_exp, nuevo_nivel
        
        return nueva_exp, nuevo_nivel

