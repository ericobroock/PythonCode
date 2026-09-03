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

        self.config_file = Path(
            CONFIG_FILE
        )

    def default_config(self):
        """Retorna uma configuração padrão."""

        return {
            "source_folder": "",
            "backup_folder": "",
            "excluded_extensions": (
                DEFAULT_EXCLUDED_EXTENSIONS.copy()
            ),
        }

    def load(self):
        """
        Carrega as configurações.

        Se o arquivo não existir, cria um novo
        com os valores padrão.
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

            # Garante que todas as configurações
            # necessárias existam.

            default = self.default_config()

            for key, value in default.items():

                if key not in config:
                    config[key] = value

            return config

        except (
            json.JSONDecodeError,
            OSError
        ):

            return self.default_config()

    def save(self, config):
        """Salva as configurações."""

        try:

            self.config_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

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