"""
ui/log_panel.py

Painel de log da aplicação.
"""

import tkinter as tk
from tkinter import ttk


class LogPanel(ttk.LabelFrame):
    """Painel que exibe mensagens do processo."""

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Log do processo",
            padding=5
        )

        self.create_widgets()

    def create_widgets(self):

        self.text = tk.Text(
            self,
            height=12,
            wrap="none",
            state="disabled",
            font=("Consolas", 9)
        )

        self.scrollbar_y = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.text.yview
        )

        self.scrollbar_x = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.text.xview
        )

        self.text.configure(
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        self.text.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Tags de cores
        self.text.tag_configure(
            "info",
            foreground="#1f4e79"
        )

        self.text.tag_configure(
            "success",
            foreground="#008000"
        )

        self.text.tag_configure(
            "warning",
            foreground="#b8860b"
        )

        self.text.tag_configure(
            "error",
            foreground="#c00000"
        )

    def add_message(self, message, level="info"):
        """Adiciona uma mensagem ao painel."""

        self.text.configure(state="normal")

        self.text.insert(
            "end",
            message + "\n",
            level
        )

        self.text.see("end")

        self.text.configure(state="disabled")

    def clear(self):
        """Limpa o painel."""

        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")