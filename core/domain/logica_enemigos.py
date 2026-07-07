import random

class Enemigos:
    def __init__(self):
        pass

    def enemigo_aleatorio_webm(self):
        enemigos_webm = {
        "orco": "./assets/bosses/webm/orc_animation.webm",
        "mariposa": "./assets/bosses/webm/butterfly_animation.webm"
        }

        

        return random.choice(list(enemigos_webm.values()))
