import pandas as pd

class DataStore:
    def __init__(self):
        self.data = pd.DataFrame()
        self.frozen_rows = set()  # índices das linhas congeladas

    def add_data(self, df: pd.DataFrame):
        """Adiciona novos dados ao dataset existente."""
        if self.data.empty:
            self.data = df.copy()
        else:
            self.data = pd.concat([self.data, df], ignore_index=True)

    def set_data(self, df: pd.DataFrame):
        """Define um novo DataFrame (usado ao carregar projetos)."""
        self.data = df.copy()

    def get_data(self) -> pd.DataFrame:
        """Retorna todos os dados, inclusive congelados."""
        return self.data

    def get_active_data(self) -> pd.DataFrame:
        """Retorna apenas as linhas que não estão congeladas."""
        if self.data.empty:
            return pd.DataFrame()
        if not self.frozen_rows:
            return self.data
        return self.data.drop(index=list(self.frozen_rows))

    def freeze_rows(self, indices: list[int]):
        """Congela linhas pelo índice."""
        self.frozen_rows.update(indices)

    def unfreeze_rows(self, indices: list[int]):
        """Descongela linhas."""
        self.frozen_rows.difference_update(indices)


# Instância global usada no app
data_store = DataStore()
