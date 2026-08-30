"""
utils/logger.py

Gerenciamento dos arquivos de log.
"""

from datetime import datetime
from pathlib import Path


class Logger:
    """Gerencia os registros da aplicação."""

    def __init__(self, log_directory=None):

        if log_directory is None:
            log_directory = (
                Path(__file__).resolve().parent.parent / "logs"
            )

        self.log_directory = Path(log_directory)

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

        self.log_file = self.log_directory / filename

        self.write("Backup iniciado.")

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

                file.write(line + "\n")

        except OSError:
            pass

    def _create_log_file(self):
        """Cria o arquivo de log sem registrar mensagem."""

        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.log"
        )

        self.log_file = self.log_directory / filename

    def finish(self):
        """Registra o encerramento."""

        self.write("Backup finalizado.")