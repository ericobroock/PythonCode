"""
config.py

Configurações gerais da aplicação.
"""

from pathlib import Path
import sys


def get_base_directory():
    """
    Retorna a pasta onde o programa está instalado/executando.

    Quando executado como .py:
        pasta do projeto.

    Quando executado como .exe:
        pasta onde está o executável.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


# Diretório base da aplicação
BASE_DIR = get_base_directory()

# Arquivo de configuração
CONFIG_FILE = BASE_DIR / "backup_config.json"

# Extensões ignoradas por padrão
DEFAULT_EXCLUDED_EXTENSIONS = [
    ".dwg",
    ".dxf",
    ".ifc",
    ".rvt",
]

# Configurações do ROBOCOPY
ROBOCOPY_RETRIES = 2
ROBOCOPY_WAIT_SECONDS = 2