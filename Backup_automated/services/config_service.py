"""
services/config_service.py

Responsável por carregar e salvar as configurações
da aplicação.
"""

import json
from pathlib import Path

from config import CONFIG_FILE, DEFAULT_EXCLUDED_EXTENSIONS


class ConfigService:
    """Gerencia as configurações do Backup Inteligente."""

    def __init__(self):
        self.config_file = Path(CONFIG_FILE)

    def default_config(self):
        """Retorna uma configuração padrão."""

        return {
            "source_folder": "",
            "backup_folder": "",
            "excluded_extensions": DEFAULT_EXCLUDED_EXTENSIONS.copy(),
        }

    def load(self):
        """
        Carrega as configurações do arquivo JSON.

        Se o arquivo não existir ou estiver inválido,
        retorna as configurações padrão.
        """

        if not self.config_file.exists():
            config = self.default_config()
            self.save(config)
            return config

        try:
            with open(
                self.config_file,
                "r",
                encoding="utf-8"
            ) as file:
                config = json.load(file)

            default = self.default_config()

            # Garante que as chaves essenciais existam
            for key, value in default.items():
                if key not in config:
                    config[key] = value

            return config

        except (json.JSONDecodeError, OSError):
            return self.default_config()

    def save(self, config):
        """Salva as configurações no arquivo JSON."""

        try:
            with open(
                self.config_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    config,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError:
            return False