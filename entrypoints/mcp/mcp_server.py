import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from mcp.server.fastmcp import FastMCP
from core.application.use_cases import TareasUseCase
from core.infrastructure.repositorios.mysql_tareas_repository import MySQLTareasRepository
from core.infrastructure.dbconfig import db_config

mcp = FastMCP("RPG-Tasks-Server")


repo = MySQLTareasRepository(db_config)
tareas_logic = TareasUseCase(repo)


@mcp.tool()
def crear_nueva_tarea(id_usuario: int, nombre: str) -> str:
    """
    Crea una nueva tarea en el RPG para un usuario específico.
    """
    
    resultado = tareas_logic.insertar_tarea(id_usuario, nombre)
    return resultado

if __name__ == "__main__":
    mcp.run(transport='stdio')