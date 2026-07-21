from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rpg_tasks.core.application.use_cases.basic_use_cases import MensajeInicioUseCase
from rpg_tasks.entrypoints.api.routers import usuarios, personajes, plataformas

app = FastAPI(title="RPG Tasks API", version="1.0.0")

app.include_router(usuarios.router)
app.include_router(personajes.router)
app.include_router(plataformas.router)



origins = [
    "http://localhost:*",  
    "http://127.0.0.1:*",
    "*",                   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
