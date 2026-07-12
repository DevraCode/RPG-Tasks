from fastapi import FastAPI
from rpg_tasks.core.application.use_cases.basic_use_cases import MensajeInicioUseCase
from rpg_tasks.entrypoints.api.routers import usuarios, plataformas

app = FastAPI(title="RPG Tasks API", version="1.0.0")

app.include_router(usuarios.router)
app.include_router(plataformas.router)

@app.get("/")
def mensaje_inicio():
    try:
        caso_uso = MensajeInicioUseCase()
        resultado = caso_uso.mensaje() 
        
        return {
            "status": "ok",
            "data": resultado
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
