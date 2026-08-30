"""
utils/threading_utils.py

Utilitários para execução de tarefas em segundo plano.
"""

import threading


def run_in_thread(target, args=(), kwargs=None, daemon=True):
    """
    Executa uma função em uma thread separada.

    Retorna o objeto Thread criado.
    """

    if kwargs is None:
        kwargs = {}

    thread = threading.Thread(
        target=target,
        args=args,
        kwargs=kwargs,
        daemon=daemon
    )

    thread.start()

    return thread