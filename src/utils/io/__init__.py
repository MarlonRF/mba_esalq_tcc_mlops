"""
Funções de I/O para carregar e salvar DataFrames.
"""
from .io_local import load_dataframe, save_dataframe

__all__ = [
    "load_dataframe",
    "save_dataframe",
]
