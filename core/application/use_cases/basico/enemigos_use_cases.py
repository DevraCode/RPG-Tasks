from core.domain.logica_enemigos import Enemigos
enemigos = Enemigos()

class EnemigosUseCase:
    def __init__(self):
        pass

    def enemigo_aleatorio_webm(self):
        return enemigos.enemigo_aleatorio_webm()