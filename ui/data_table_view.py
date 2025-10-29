from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor

class DataTableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(0)
        self.setRowCount(0)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.selected_rows = set()

        self.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #0078D7;
                color: white;
            }
        """)


    def update_table(self, df, frozen_rows=None):
        """Atualiza tabela, destacando linhas congeladas e selecionadas."""
        frozen_rows = frozen_rows or set()
        # Salva seleção atual
        self.selected_rows = set(idx.row() for idx in self.selectedIndexes())

        self.setColumnCount(len(df.columns))
        self.setRowCount(len(df))
        self.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                value = str(df.iloc[i, j])
                item = QTableWidgetItem(value)

                # Linha congelada em cinza
                if i in frozen_rows:
                    item.setBackground(QColor(200, 200, 200))  # cinza claro                

                self.setItem(i, j, item)

        # Reaplica seleção das linhas
        for row in self.selected_rows:
            self.selectRow(row)

    def get_selected_indices(self):
        """Retorna índices das linhas selecionadas."""
        return list(set(idx.row() for idx in self.selectedIndexes()))
