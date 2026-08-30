"""
config.py

Configurações gerais da aplicação.
"""

from pathlib import Path


# Diretório onde o programa está sendo executado
BASE_DIR = Path(__file__).resolve().parent

# Arquivo de configuração
CONFIG_FILE = BASE_DIR / "backup_config.json"

# Extensões ignoradas por padrão
DEFAULT_EXCLUDED_EXTENSIONS = [
    ".dwg",
    ".dxf",
    ".ifc",
    ".rvt",
]

# Configurações padrão do ROBOCOPY
ROBOCOPY_RETRIES = 2
ROBOCOPY_WAIT_SECONDS = 2