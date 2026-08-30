"""
services/robocopy_runner.py

Executa o ROBOCOPY e interpreta sua saída.
"""

import subprocess


class RobocopyRunner:
    """Executa comandos ROBOCOPY."""

    def __init__(self):
        self.process = None

    def build_command(
        self,
        source,
        destination,
        excluded_extensions
    ):
        """
        Monta o comando ROBOCOPY.
        """

        command = [
            "robocopy",
            str(source),
            str(destination),

            # Inclui subpastas
            "/E",

            # Não copia arquivos mais antigos
            "/XO",

            # Tolerância de diferença de horário em sistemas de rede
            "/FFT",

            # Tentativas em caso de erro
            "/R:2",

            # Tempo entre tentativas
            "/W:2",

            # Mostra o progresso
            "/ETA",

            # Não exibe cabeçalho
            "/NJH",

            # Não exibe resumo final
            "/NJS",

            # Não exibe progresso por arquivo
            "/NP",
        ]

        # Adiciona as extensões excluídas
        if excluded_extensions:

            command.append("/XF")

            for extension in excluded_extensions:

                extension = extension.strip()

                if not extension:
                    continue

                if not extension.startswith("."):
                    extension = "." + extension

                command.append(f"*{extension}")

        return command

    def run(
        self,
        source,
        destination,
        excluded_extensions,
        output_callback=None
    ):
        """
        Executa o ROBOCOPY.

        output_callback recebe cada linha produzida pelo processo.
        """

        command = self.build_command(
            source,
            destination,
            excluded_extensions
        )

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="cp850",
            errors="replace",
            bufsize=1
        )

        for line in self.process.stdout:

            line = line.rstrip()

            if line and output_callback:
                output_callback(line)

        return_code = self.process.wait()

        self.process = None

        return return_code

    def cancel(self):
        """Interrompe o ROBOCOPY em execução."""

        if self.process is not None:

            try:
                self.process.terminate()
            except OSError:
                pass

            self.process = None