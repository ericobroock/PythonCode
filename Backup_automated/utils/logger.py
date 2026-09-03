"""
utils/logger.py

Gerenciamento dos arquivos de log.
"""

from datetime import datetime
from pathlib import Path
import sys


class Logger:
    """Gerencia os registros da aplicação."""

    def __init__(self, log_directory=None):

        if log_directory is None:

            # Quando executado como .exe
            if getattr(sys, "frozen", False):

                base_directory = Path(
                    sys.executable
                ).resolve().parent

            # Quando executado como .py
            else:

                base_directory = (
                    Path(__file__)
                    .resolve()
                    .parent
                    .parent
                )

            log_directory = (
                base_directory / "logs"
            )

        self.log_directory = Path(
            log_directory
        )

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.log_file = None

    def start(self):
        """Inicia um novo arquivo de log."""

        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.log"
        )

        self.log_file = (
            self.log_directory / filename
        )

        self.write(
            "Backup iniciado."
        )

    def write(self, message):
        """
        Grava uma mensagem no arquivo de log.

        Linhas vazias não são gravadas.
        """

        if not message:
            return

        message = str(message).strip()

        if not message:
            return

        if self.log_file is None:
            self._create_log_file()

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        line = f"[{timestamp}] {message}"

        try:

            with open(
                self.log_file,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    line + "\n"
                )

        except OSError:
            pass

    def _create_log_file(self):
        """Cria o arquivo de log."""

        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.log"
        )

        self.log_file = (
            self.log_directory / filename
        )

    def finish(self):
        """Registra o encerramento."""

        self.write(
            "Backup finalizado."
        )

    def get_log_directory(self):
        """Retorna a pasta onde os logs são armazenados."""

        return self.log_directory

    def get_log_file(self):
        """Retorna o arquivo de log atual."""

        return self.log_file