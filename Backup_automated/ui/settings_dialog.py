"""
ui/settings_dialog.py

Janela de configurações do Backup Inteligente.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class SettingsDialog(tk.Toplevel):
    """Janela de configurações."""

    def __init__(self, parent, config):

        super().__init__(parent)

        self.parent = parent
        self.config = config.copy()

        self.result = None

        self.title("Configurações")
        self.geometry("500x400")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_cancel
        )

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
            text="Configurações do Backup",
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # -------------------------------------------------
        # Extensões
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Extensões que NÃO serão copiadas:"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            main,
            text=(
                "Informe uma extensão por linha. "
                "O ponto inicial é opcional."
            )
        ).pack(
            anchor="w",
            pady=(2, 8)
        )

        frame_extensions = ttk.Frame(main)

        frame_extensions.pack(
            fill="both",
            expand=True
        )

        self.listbox = tk.Listbox(
            frame_extensions,
            height=10,
            font=("Consolas", 10)
        )

        scrollbar = ttk.Scrollbar(
            frame_extensions,
            orient="vertical",
            command=self.listbox.yview
        )

        self.listbox.configure(
            yscrollcommand=scrollbar.set
        )

        self.listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for extension in self.config.get(
            "excluded_extensions",
            []
        ):

            self.listbox.insert(
                "end",
                extension
            )

        # -------------------------------------------------
        # Campo adicionar
        # -------------------------------------------------

        add_frame = ttk.Frame(main)

        add_frame.pack(
            fill="x",
            pady=10
        )

        self.entry_extension = ttk.Entry(
            add_frame
        )

        self.entry_extension.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.entry_extension.bind(
            "<Return>",
            lambda event: self.add_extension()
        )

        ttk.Button(
            add_frame,
            text="Adicionar",
            command=self.add_extension
        ).pack(
            side="left",
            padx=(5, 0)
        )

        ttk.Button(
            add_frame,
            text="Remover",
            command=self.remove_extension
        ).pack(
            side="left",
            padx=(5, 0)
        )

        # -------------------------------------------------
        # Botões
        # -------------------------------------------------

        buttons = ttk.Frame(main)

        buttons.pack(
            fill="x",
            pady=(10, 0)
        )

        ttk.Button(
            buttons,
            text="Restaurar padrão",
            command=self.restore_defaults
        ).pack(
            side="left"
        )

        ttk.Button(
            buttons,
            text="Cancelar",
            command=self.on_cancel
        ).pack(
            side="right",
            padx=(5, 0)
        )

        ttk.Button(
            buttons,
            text="OK",
            command=self.on_ok
        ).pack(
            side="right"
        )

    def add_extension(self):

        extension = self.entry_extension.get().strip()

        if not extension:
            return

        if not extension.startswith("."):
            extension = "." + extension

        extension = extension.lower()

        existing = [
            self.listbox.get(i).lower()
            for i in range(self.listbox.size())
        ]

        if extension in existing:

            messagebox.showwarning(
                "Extensão existente",
                f"A extensão {extension} já está cadastrada.",
                parent=self
            )

            return

        self.listbox.insert(
            "end",
            extension
        )

        self.entry_extension.delete(
            0,
            "end"
        )

    def remove_extension(self):

        selection = self.listbox.curselection()

        if not selection:
            return

        for index in reversed(selection):

            self.listbox.delete(index)

    def restore_defaults(self):

        answer = messagebox.askyesno(
            "Restaurar padrão",
            "Deseja restaurar as extensões padrão?",
            parent=self
        )

        if not answer:
            return

        self.listbox.delete(
            0,
            "end"
        )

        defaults = [
            ".dwg",
            ".dxf",
            ".ifc",
            ".rvt"
        ]

        for extension in defaults:

            self.listbox.insert(
                "end",
                extension
            )

    def on_ok(self):

        extensions = [
            self.listbox.get(i)
            for i in range(self.listbox.size())
        ]

        self.result = self.config.copy()

        self.result[
            "excluded_extensions"
        ] = extensions

        self.destroy()

    def on_cancel(self):

        self.result = None

        self.destroy()