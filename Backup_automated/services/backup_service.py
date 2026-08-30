"""
services/backup_service.py

Coordena a execução do backup.
"""

from pathlib import Path

from services.robocopy_runner import RobocopyRunner


class BackupService:
    """Serviço responsável pelo processo de backup."""

    def __init__(self):
        self.runner = RobocopyRunner()

    def validate(self, source, destination):
        """
        Valida as pastas antes de iniciar o backup.
        """

        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            raise ValueError(
                "A pasta de origem não existe."
            )

        if not source.is_dir():
            raise ValueError(
                "A origem informada não é uma pasta."
            )

        if str(source).strip() == str(destination).strip():
            raise ValueError(
                "A pasta de origem e a pasta de backup "
                "não podem ser iguais."
            )

        return True

    def run(
        self,
        source,
        destination,
        excluded_extensions,
        output_callback=None
    ):
        """
        Executa o backup.
        """

        self.validate(source, destination)

        return self.runner.run(
            source=source,
            destination=destination,
            excluded_extensions=excluded_extensions,
            output_callback=output_callback
        )

    def cancel(self):
        """Cancela o backup atual."""

        self.runner.cancel()

    @staticmethod
    def is_success(return_code):
        """
        Verifica se o código de retorno do ROBOCOPY
        representa uma execução bem-sucedida.

        Códigos 0 a 3 são considerados sucesso.
        """

        return return_code <= 3