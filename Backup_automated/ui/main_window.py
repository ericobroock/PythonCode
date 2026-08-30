"""
ui/main_window.py

Janela principal do Backup Inteligente.
"""

import os
import threading
import tkinter as tk

from pathlib import Path
from tkinter import ttk, filedialog, messagebox

from config import DEFAULT_EXCLUDED_EXTENSIONS
from services.backup_service import BackupService
from services.config_service import ConfigService
from utils.logger import Logger
from ui.log_panel import LogPanel
from ui.settings_dialog import SettingsDialog


class MainWindow(tk.Tk):
    """Janela principal da aplicação."""

    def __init__(self):

        super().__init__()

        self.title("Backup Inteligente")
        self.geometry("800x650")
        self.minsize(700, 550)

        self.config_service = ConfigService()

        self.config_data = (
            self.config_service.load()
        )

        self.backup_service = BackupService()

        self.logger = Logger()

        self.backup_running = False

        self.total_files = 0
        self.processed_files = 0
        self.copied_files = 0

        self.create_menu()
        self.create_widgets()

        self.load_configuration()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # =====================================================
    # MENU
    # =====================================================

    def create_menu(self):

        menubar = tk.Menu(self)

        # -------------------------------------------------
        # Arquivo
        # -------------------------------------------------

        menu_file = tk.Menu(
            menubar,
            tearoff=False
        )

        menu_file.add_command(
            label="Sair",
            command=self.on_close
        )

        menubar.add_cascade(
            label="Arquivo",
            menu=menu_file
        )

        # -------------------------------------------------
        # Ferramentas
        # -------------------------------------------------

        menu_tools = tk.Menu(
            menubar,
            tearoff=False
        )

        menu_tools.add_command(
            label="Configurações",
            command=self.open_settings
        )

        menubar.add_cascade(
            label="Ferramentas",
            menu=menu_tools
        )

        # -------------------------------------------------
        # Ajuda
        # -------------------------------------------------

        menu_help = tk.Menu(
            menubar,
            tearoff=False
        )

        menu_help.add_command(
            label="Sobre",
            command=self.show_about
        )

        menubar.add_cascade(
            label="Ajuda",
            menu=menu_help
        )

        self.config(
            menu=menubar
        )

    # =====================================================
    # INTERFACE
    # =====================================================

    def create_widgets(self):

        main = ttk.Frame(
            self,
            padding=15
        )

        main.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Título
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Backup Inteligente",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w"
        )

        ttk.Label(
            main,
            text=(
                "Copie somente arquivos novos ou modificados "
                "para o servidor."
            )
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # -------------------------------------------------
        # Origem
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Pasta de origem:"
        ).pack(
            anchor="w"
        )

        source_frame = ttk.Frame(main)

        source_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        self.source_var = tk.StringVar()

        self.source_entry = ttk.Entry(
            source_frame,
            textvariable=self.source_var
        )

        self.source_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            source_frame,
            text="Escolher...",
            command=self.choose_source
        ).pack(
            side="left",
            padx=(5, 0)
        )

        # -------------------------------------------------
        # Destino
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Pasta de backup / servidor:"
        ).pack(
            anchor="w"
        )

        destination_frame = ttk.Frame(main)

        destination_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        self.destination_var = tk.StringVar()

        self.destination_entry = ttk.Entry(
            destination_frame,
            textvariable=self.destination_var
        )

        self.destination_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            destination_frame,
            text="Escolher...",
            command=self.choose_destination
        ).pack(
            side="left",
            padx=(5, 0)
        )

        # -------------------------------------------------
        # Extensões
        # -------------------------------------------------

        extensions_frame = ttk.LabelFrame(
            main,
            text="Extensões ignoradas",
            padding=10
        )

        extensions_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.extensions_var = tk.StringVar()

        ttk.Label(
            extensions_frame,
            textvariable=self.extensions_var
        ).pack(
            anchor="w"
        )

        # -------------------------------------------------
        # Progresso
        # -------------------------------------------------

        progress_frame = ttk.LabelFrame(
            main,
            text="Progresso",
            padding=10
        )

        progress_frame.pack(
            fill="x"
        )

        self.progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )

        self.progress.pack(
            fill="x"
        )

        self.progress_label = ttk.Label(
            progress_frame,
            text="Aguardando backup..."
        )

        self.progress_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Botões
        # -------------------------------------------------

        buttons = ttk.Frame(main)

        buttons.pack(
            fill="x",
            pady=15
        )

        self.start_button = ttk.Button(
            buttons,
            text="Iniciar Backup",
            command=self.start_backup
        )

        self.start_button.pack(
            side="left"
        )

        self.cancel_button = ttk.Button(
            buttons,
            text="Cancelar",
            command=self.cancel_backup,
            state="disabled"
        )

        self.cancel_button.pack(
            side="left",
            padx=10
        )

        self.clear_button = ttk.Button(
            buttons,
            text="Limpar Log",
            command=self.clear_log
        )

        self.clear_button.pack(
            side="right"
        )

        # -------------------------------------------------
        # Log
        # -------------------------------------------------

        self.log_panel = LogPanel(main)

        self.log_panel.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        self.status_var = tk.StringVar(
            value="Pronto."
        )

        ttk.Label(
            main,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w"
        ).pack(
            fill="x",
            pady=(10, 0)
        )

    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================

    def load_configuration(self):

        self.source_var.set(
            self.config_data.get(
                "source_folder",
                ""
            )
        )

        self.destination_var.set(
            self.config_data.get(
                "backup_folder",
                ""
            )
        )

        self.update_extensions_label()

    def save_configuration(self):

        self.config_data[
            "source_folder"
        ] = self.source_var.get().strip()

        self.config_data[
            "backup_folder"
        ] = self.destination_var.get().strip()

        self.config_service.save(
            self.config_data
        )

    def update_extensions_label(self):

        extensions = self.config_data.get(
            "excluded_extensions",
            DEFAULT_EXCLUDED_EXTENSIONS
        )

        if extensions:

            self.extensions_var.set(
                "   ".join(extensions)
            )

        else:

            self.extensions_var.set(
                "Nenhuma extensão configurada."
            )

    # =====================================================
    # ESCOLHA DE PASTAS
    # =====================================================

    def choose_source(self):

        folder = filedialog.askdirectory(
            title="Selecione a pasta de origem"
        )

        if folder:

            self.source_var.set(folder)

            self.save_configuration()

    def choose_destination(self):

        folder = filedialog.askdirectory(
            title="Selecione a pasta de backup"
        )

        if folder:

            self.destination_var.set(folder)

            self.save_configuration()

    # =====================================================
    # CONFIGURAÇÕES
    # =====================================================

    def open_settings(self):

        dialog = SettingsDialog(
            self,
            self.config_data
        )

        self.wait_window(dialog)

        if dialog.result is not None:

            self.config_data = dialog.result

            self.save_configuration()

            self.update_extensions_label()

            self.add_log(
                "Configurações atualizadas.",
                "success"
            )

    # =====================================================
    # BACKUP
    # =====================================================

    def start_backup(self):

        if self.backup_running:
            return

        source = self.source_var.get().strip()
        destination = self.destination_var.get().strip()

        if not source:

            messagebox.showwarning(
                "Origem",
                "Selecione a pasta de origem.",
                parent=self
            )

            return

        if not destination:

            messagebox.showwarning(
                "Destino",
                "Selecione a pasta de backup.",
                parent=self
            )

            return

        if not Path(source).exists():

            messagebox.showerror(
                "Erro",
                "A pasta de origem não existe.",
                parent=self
            )

            return

        # Salva configurações
        self.save_configuration()

        # Limpa progresso
        self.progress["value"] = 0

        self.processed_files = 0
        self.total_files = 0
        self.copied_files = 0

        self.backup_running = True

        self.start_button.config(
            state="disabled"
        )

        self.cancel_button.config(
            state="normal"
        )

        self.status_var.set(
            "Analisando arquivos..."
        )

        self.add_log(
            "Iniciando análise dos arquivos...",
            "info"
        )

        thread = threading.Thread(
            target=self.backup_worker,
            daemon=True
        )

        thread.start()

    def backup_worker(self):

        try:

            source = Path(
                self.source_var.get().strip()
            )

            destination = Path(
                self.destination_var.get().strip()
            )

            excluded = self.config_data.get(
                "excluded_extensions",
                DEFAULT_EXCLUDED_EXTENSIONS
            )

            self.logger.start()

            self.logger.write(
                f"Origem: {source}"
            )

            self.logger.write(
                f"Destino: {destination}"
            )

            self.logger.write(
                "Extensões ignoradas: "
                + (
                    ", ".join(excluded)
                    if excluded
                    else "nenhuma"
                )
)

            # -------------------------------------------------
            # Análise
            # -------------------------------------------------

            eligible_files = []

            for root, dirs, files in os.walk(source):

                for filename in files:

                    extension = Path(
                        filename
                    ).suffix.lower()

                    if extension in [
                        ext.lower()
                        for ext in excluded
                    ]:
                        continue

                    eligible_files.append(
                        Path(root) / filename
                    )

            self.total_files = len(
                eligible_files
            )

            self.logger.write(
                f"Arquivos elegíveis para cópia: {self.total_files}"
            )

            self.after(
                0,
                self.analysis_finished,
                self.total_files
            )

            # self.logger.write(
            #     f"Arquivos elegíveis encontrados: {self.total_files}"
            # )

            self.logger.write(
                "Backup em execução."
            )

            # -------------------------------------------------
            # Backup
            # -------------------------------------------------

            return_code = (
                self.backup_service.run(
                    source=source,
                    destination=destination,
                    excluded_extensions=excluded,
                    output_callback=self.robocopy_output
                )
            )

            self.after(
                0,
                self.backup_finished,
                return_code
            )

        except Exception as error:

            self.after(
                0,
                self.backup_error,
                str(error)
            )

    # =====================================================
    # ANÁLISE
    # =====================================================

    def analysis_finished(self, total):

        self.total_files = total

        self.add_log(
            f"Arquivos elegíveis encontrados: {total}",
            "info"
        )

        if total == 0:

            self.progress_label.config(
                text="Nenhum arquivo elegível encontrado."
            )

        else:

            self.progress_label.config(
                text=f"0 de {total} arquivos"
            )

        self.status_var.set(
            "Executando backup..."
        )

    # =====================================================
    # SAÍDA DO ROBOCOPY
    # =====================================================

    def robocopy_output(self, line):
        """
        Recebe a saída do ROBOCOPY.

        A saída original é enviada para a interface.
        O log recebe apenas linhas úteis.
        """

        line = line.strip()

        if not line:
            return

        self.after(
            0,
            self.process_robocopy_line,
            line
        )

    def process_robocopy_line(self, line):

        line = line.strip()

        if not line:
            return

        # -------------------------------------------------
        # Resumo do ROBOCOPY
        # -------------------------------------------------

        if line.startswith("Files"):

            parts = line.split()

            try:
                self.copied_files = int(parts[2])

            except (IndexError, ValueError):
                pass

            # Não exibe o resumo técnico na tela
            return

        # -------------------------------------------------
        # Outras linhas do resumo
        # -------------------------------------------------

        if (
            line.startswith("Dirs")
            or line.startswith("Bytes")
            or line.startswith("Times")
            or line.startswith("Ended")
            or line.startswith("Diretórios")
            or line.startswith("Arquivos")
            or line.startswith("Bytes")
            or line.startswith("N.º de Vezes")
            or line.startswith("Finalizado em")
            or line.startswith("Total")
            or line.startswith("=")
        ):
            return

        # -------------------------------------------------
        # Linhas de arquivos
        # -------------------------------------------------

        looks_like_file = (
            "." in line
            and not line.startswith("ROBOCOPY")
            and not line.startswith(
                "-------------------------------------------------------------------------------"
            )
        )

        if looks_like_file:

            self.processed_files += 1

            if self.total_files > 0:

                percentage = (
                    self.processed_files
                    / self.total_files
                    * 100
                )

                percentage = min(
                    percentage,
                    100
                )

                self.progress["value"] = percentage

                self.progress_label.config(
                    text=(
                        f"{self.processed_files} de "
                        f"{self.total_files} arquivos "
                        f"({percentage:.0f}%)"
                    )
                )

            # Exibe na tela
            self.add_log(
                line,
                "success"
            )

            # Grava no arquivo
            self.logger.write(
                f"Arquivo processado: {line}"
            )

        else:

            self.add_log(
                line,
                "info"
            )

    # =====================================================
    # FINALIZAÇÃO
    # =====================================================

    def backup_finished(self, return_code):

        self.backup_running = False

        self.start_button.config(
            state="normal"
        )

        self.cancel_button.config(
            state="disabled"
        )

        self.logger.write(
            f"Arquivos copiados: {self.copied_files}"
        )

        self.add_log(
            f"Arquivos copiados: {self.copied_files}",
            "success"
        )

        self.logger.finish()

        if self.backup_service.is_success(
            return_code
        ):

            self.progress["value"] = 100

            self.status_var.set(
                "Backup concluído com sucesso."
            )

            self.progress_label.config(
                text="Backup concluído — 100%"
            )

            self.add_log(
                "========================================",
                "success"
            )

            self.add_log(
                f"Backup concluído. Código ROBOCOPY: {return_code}",
                "success"
            )

            messagebox.showinfo(
                "Backup concluído",
                "O backup foi concluído com sucesso.",
                parent=self
            )

        else:

            self.status_var.set(
                "Backup concluído com ocorrências."
            )

            self.add_log(
                (
                    "Backup finalizado com código "
                    f"ROBOCOPY: {return_code}"
                ),
                "warning"
            )

            messagebox.showwarning(
                "Backup",
                (
                    "O ROBOCOPY terminou com ocorrências.\n\n"
                    f"Código de retorno: {return_code}\n\n"
                    "Consulte o log para mais detalhes."
                ),
                parent=self
            )

    def backup_error(self, error):

        self.backup_running = False

        self.start_button.config(
            state="normal"
        )

        self.cancel_button.config(
            state="disabled"
        )

        self.status_var.set(
            "Erro durante o backup."
        )

        self.add_log(
            f"ERRO: {error}",
            "error"
        )

        messagebox.showerror(
            "Erro",
            f"Ocorreu um erro durante o backup:\n\n{error}",
            parent=self
        )

    # =====================================================
    # CANCELAR
    # =====================================================

    def cancel_backup(self):

        if not self.backup_running:
            return

        answer = messagebox.askyesno(
            "Cancelar backup",
            "Deseja realmente cancelar o backup?",
            parent=self
        )

        if not answer:
            return

        self.add_log(
            "Cancelando backup...",
            "warning"
        )

        self.backup_service.cancel()

        self.backup_running = False

        self.start_button.config(
            state="normal"
        )

        self.cancel_button.config(
            state="disabled"
        )

        self.status_var.set(
            "Backup cancelado."
        )

        self.add_log(
            "Backup cancelado pelo usuário.",
            "warning"
        )

    # =====================================================
    # LOG
    # =====================================================

    def add_log(self, message, level="info"):

        self.log_panel.add_message(
            message,
            level
        )

    def clear_log(self):

        self.log_panel.clear()

        self.status_var.set(
            "Log limpo."
        )

    # =====================================================
    # SOBRE
    # =====================================================

    def show_about(self):

        messagebox.showinfo(
            "Sobre",
            (
                "Backup Inteligente\n\n"
                "Versão 1.0\n\n"
                "Sistema de backup incremental utilizando "
                "ROBOCOPY."
            ),
            parent=self
        )

    # =====================================================
    # ENCERRAMENTO
    # =====================================================

    def on_close(self):

        if self.backup_running:

            answer = messagebox.askyesno(
                "Backup em andamento",
                (
                    "Existe um backup em andamento.\n\n"
                    "Deseja cancelar e fechar o programa?"
                ),
                parent=self
            )

            if not answer:
                return

            self.backup_service.cancel()

        self.save_configuration()

        self.destroy()