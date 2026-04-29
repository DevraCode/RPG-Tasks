import sys
import os

# Añade la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))



from mcp.server.fastmcp import FastMCP
from core.application.use_cases import TareasUseCase
from core.infrastructure.mysql_tareas_repository import MySQLTareasRepository
from core.infrastructure.dbconfig import db_config

# 1. Inicializar FastMCP
mcp = FastMCP("RPG-Tasks-Server")

# 2. Configurar dependencias
repo = MySQLTareasRepository(db_config)
tareas_logic = TareasUseCase(repo)

# 3. Exponer una herramienta (Tool)
@mcp.tool()
def crear_nueva_tarea(id_usuario: int, nombre: str) -> str:
    """
    Crea una nueva tarea en el RPG para un usuario específico.
    """
    # Llamamos a tu lógica existente
    resultado = tareas_logic.insertar_tarea(id_usuario, nombre)
    return resultado

if __name__ == "__main__":
    mcp.run(transport='stdio')