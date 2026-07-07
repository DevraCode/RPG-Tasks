from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


from entrypoints.web_app.routes import tareas_routes, personajes_routes 

app = FastAPI()
templates = Jinja2Templates(directory="entrypoints/web_app/templates")
templates.env.cache = None

#app.include_router(tareas_routes.router)
#app.include_router(personajes_routes.router)

@app.get("/")
async def index(request: Request):
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"mensaje": "Bienvenido"}
    )














