# core/importer/file_importer.py
import pandas as pd
from core.importer.layouts import LAYOUTS
from io import StringIO

def import_files(file_paths, layout_name):
    layout = LAYOUTS.get(layout_name)
    if not layout:
        raise ValueError(f"Layout '{layout_name}' não encontrado.")

    all_data = []

    for file_path in file_paths:
        # 🔍 Lê conteúdo com fallback de encoding
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()

        # 🔍 Detecta delimitador (mais usado)
        delimiter = ";" if content.count(";") > content.count(",") else ","

        # 🔍 Identifica linha de cabeçalho válida
        lines = content.splitlines()
        header_index = None
        for i, line in enumerate(lines):
            if any(col in line for col in layout["columns"].keys()):
                header_index = i
                break
        if header_index is None:
            raise ValueError(f"Nenhum cabeçalho compatível encontrado em {file_path}")

        # 🔍 Mantém apenas linhas de dados (até bloco tipo [System])
        data_lines = []
        for line in lines[header_index:]:
            if line.strip().startswith("["):
                break
            if line.strip():
                data_lines.append(line)

        if not data_lines:
            continue

        # 🔍 Lê o CSV efetivamente
        df = pd.read_csv(
            StringIO("\n".join(data_lines)),
            delimiter=delimiter,
            engine="python",
            encoding="utf-8",
            on_bad_lines="skip"
        )

        # 🔍 Renomeia colunas conforme layout
        mapping = layout["columns"]
        df = df.rename(columns=mapping)

        # 🔍 Filtra apenas as colunas conhecidas
        df = df[[c for c in mapping.values() if c in df.columns]]

        if not df.empty:
            all_data.append(df)

    if not all_data:
        raise ValueError("Nenhum dado válido importado.")

    data = pd.concat(all_data, ignore_index=True)

    # 🔍 Converte e ordena datetime
    if "datetime" in data.columns:
        data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")
        data = data.dropna(subset=["datetime"]).sort_values(by="datetime").reset_index(drop=True)

    return data
