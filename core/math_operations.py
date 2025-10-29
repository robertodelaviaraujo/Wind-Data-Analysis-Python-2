# core/math_operations.py
import pandas as pd

def calculate_mean(df: pd.DataFrame, columns: list[str] = None) -> dict:
    """
    Calcula a média das colunas especificadas.
    Se columns for None, usa todas as colunas numéricas.
    Retorna um dicionário {coluna: media}.
    """
    columns = columns or df.select_dtypes(include="number").columns.tolist()
    return df[columns].mean().to_dict()

def calculate_std(df: pd.DataFrame, columns: list[str] = None) -> dict:
    """
    Calcula o desvio padrão das colunas especificadas.
    Se columns for None, usa todas as colunas numéricas.
    Retorna um dicionário {coluna: std}.
    """
    columns = columns or df.select_dtypes(include="number").columns.tolist()
    return df[columns].std().to_dict()

def calculate_correlation(df: pd.DataFrame, col_x: str, col_y: str) -> float:
    """
    Calcula a correlação entre duas colunas numéricas.
    Retorna um float.
    """
    if col_x not in df.columns or col_y not in df.columns:
        raise ValueError(f"Colunas {col_x} ou {col_y} não existem no dataframe.")
    return df[[col_x, col_y]].corr().iloc[0, 1]
