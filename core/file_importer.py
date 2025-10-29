import pandas as pd
from core.importer.layouts import LAYOUTS

def import_files(file_paths, layout_name):
    """
    Importa um ou mais arquivos conforme o layout selecionado.
    Ignora blocos fora do padrão tabular (ex: seções [System], [Summary], etc.).
    """
    layout = LAYOUTS.get(layout_name)
    if not layout:
        raise ValueError(f"Layout '{layout_name}' não encontrado.")

    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                lines = f.readlines()

        # 🔍 Detecta onde o bloco de dados realmente começa
        header_index = None
        for i, line in enumerate(lines):
            if any(col in line for col in layout["columns"].keys()):
                header_index = i
                break

        if header_index is None:
            raise ValueError(f"Nenhum cabeçalho compatível encontrado em {file_path}")

        # 🔍 Mantém apenas linhas que seguem o padrão (antes de blocos como [System])
        data_lines = []
        for line in lines[header_index:]:
            if line.strip().startswith("["):
                # Parar quando encontrar bloco tipo [System], [Summary], etc.
                break
            # Ignorar linhas totalmente vazias
            if not line.strip():
                continue
            data_lines.append(line)

        if not data_lines:
            continue

        # Detecta delimitador
        sample = "".join(data_lines[:10])
        delimiter = ";" if sample.count(";") > sample.count(",") else ","

        from io import StringIO
        try:
            df = pd.read_csv(
                StringIO("".join(data_lines)),
                delimiter=delimiter,
                engine="python",
                encoding="utf-8",
                on_bad_lines="skip"
            )
        except Exception as e:
            raise ValueError(f"Erro ao ler {file_path}: {e}")

        # Renomeia colunas com base no layout
        column_mapping = layout["columns"]
        df = df.rename(columns=column_mapping)

        # Filtra apenas colunas conhecidas
        df = df[[c for c in column_mapping.values() if c in df.columns]]

        # Apenas adiciona se houver dados válidos
        if not df.empty:
            all_data.append(df)

    if not all_data:
        raise ValueError("Nenhum dado válido importado.")

    # Junta todos os DataFrames
    data = pd.concat(all_data, ignore_index=True)

    # Converte e ordena por datetime
    if "datetime" in data.columns:
        data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")
        data = data.dropna(subset=["datetime"]).sort_values(by="datetime").reset_index(drop=True)

    return data
