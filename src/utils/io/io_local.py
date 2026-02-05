"""
Carrega um DataFrame de um caminho local ou URL.
"""
import io
import os
import pandas as pd
import requests


def _read_csv_robust(file_path_or_buffer) -> pd.DataFrame:
    """Lê CSV com detecção automática de delimitador e tratamento robusto de erros."""
    import csv as _csv

    # Se for string (caminho), detecta delimitador do arquivo
    if isinstance(file_path_or_buffer, str):
        delim = ","
        try:
            with open(file_path_or_buffer, 'r', encoding='utf-8') as f:
                sample = f.read(4096)
                sniff = _csv.Sniffer()
                delim = sniff.sniff(sample).delimiter
        except Exception:
            delim = ","
        
        # Tenta ler com engine python (mais permissivo)
        try:
            return pd.read_csv(file_path_or_buffer, delimiter=delim, engine="python")
        except Exception:
            try:
                return pd.read_csv(file_path_or_buffer, delimiter=delim, on_bad_lines="warn")
            except TypeError:
                # pandas antigo
                return pd.read_csv(file_path_or_buffer, delimiter=delim, error_bad_lines=False)
    
    # Se for buffer (BytesIO, StringIO), usa o método original
    else:
        delim = ","
        try:
            sample = file_path_or_buffer.read(4096)
            if isinstance(sample, bytes):
                sample = sample.decode("utf-8", errors="replace")
            sniff = _csv.Sniffer()
            delim = sniff.sniff(sample).delimiter
        except Exception:
            delim = ","

        # Reseta buffer e lê
        try:
            file_path_or_buffer.seek(0)
            return pd.read_csv(file_path_or_buffer, delimiter=delim, engine="python")
        except Exception:
            try:
                file_path_or_buffer.seek(0)
                return pd.read_csv(file_path_or_buffer, delimiter=delim, on_bad_lines="warn")
            except TypeError:
                file_path_or_buffer.seek(0)
                return pd.read_csv(file_path_or_buffer, delimiter=delim, error_bad_lines=False)


def load_dataframe(path_or_buffer: str, **kwargs) -> pd.DataFrame:
    """Carrega um DataFrame de um caminho local ou URL.

    Suporta: .csv, .xls/.xlsx, .feather, .parquet, .pkl/.pickle
    Se for uma URL (http/https), faz download temporário e carrega.
    """
    # Verifica se é URL
    if path_or_buffer.startswith(("http://", "https://")):
        resp = requests.get(path_or_buffer, timeout=30)
        resp.raise_for_status()
        buffer = io.BytesIO(resp.content)
        ext = path_or_buffer.split(".")[-1].lower()
    else:
        # Resolve caminho relativo de forma inteligente
        from pathlib import Path
        
        # Se for caminho relativo, tenta a partir do diretório atual primeiro
        path = Path(path_or_buffer)
        if not path.is_absolute() and not path.exists():
            # Tenta a partir do diretório pai (útil para notebooks/)
            parent_path = Path.cwd().parent / path_or_buffer
            if parent_path.exists():
                path = parent_path
            else:
                # Mantém o caminho original (deixa falhar com erro claro)
                path = Path(path_or_buffer)
        
        buffer = str(path)
        ext = path.suffix.lower().replace(".", "")

    # Lê conforme extensão
    if ext in ("csv", "txt"):
        return _read_csv_robust(buffer)
    elif ext in ("xls", "xlsx"):
        return pd.read_excel(buffer, **kwargs)
    elif ext == "feather":
        return pd.read_feather(buffer, **kwargs)
    elif ext == "parquet":
        return pd.read_parquet(buffer, **kwargs)
    elif ext in ("pkl", "pickle"):
        return pd.read_pickle(buffer, **kwargs)
    else:
        raise ValueError(f"Formato não suportado: {ext}")


def save_dataframe(df: pd.DataFrame, path: str, **kwargs):
    """Salva um DataFrame em arquivo local conforme extensão."""
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    
    if ext == "csv":
        df.to_csv(path, index=False, **kwargs)
    elif ext in ("xls", "xlsx"):
        df.to_excel(path, index=False, **kwargs)
    elif ext == "feather":
        df.to_feather(path, **kwargs)
    elif ext == "parquet":
        df.to_parquet(path, **kwargs)
    elif ext in ("pkl", "pickle"):
        df.to_pickle(path, **kwargs)
    else:
        raise ValueError(f"Formato não suportado: {ext}")
