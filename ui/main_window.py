from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QLabel
)
from ui.data_table_view import DataTableView
from ui.graph_panel import GraphPanel
from ui.dialogs.layout_selector_dialog import LayoutSelectorDialog
from core.file_importer import import_files
from core.data_store import data_store
import core.math_operations as mo
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌬️ Wind Analyzer - Software de Anemometria")
        self.resize(1400, 800)

        # -------------------
        # Layout principal
        # -------------------
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Tabela de dados
        self.table = DataTableView()
        main_layout.addWidget(self.table, 3)

        # Painel de gráficos
        self.graph_panel = GraphPanel()
        main_layout.addWidget(self.graph_panel, 4)

        # -------------------
        # Layout lateral: botões e cálculos
        # -------------------
        button_layout = QVBoxLayout()

        # Botões principais
        btn_import = QPushButton("📂 Importar Arquivos")
        btn_save = QPushButton("💾 Salvar Projeto (.wnd)")
        btn_load = QPushButton("📁 Abrir Projeto (.wnd)")
        btn_freeze = QPushButton("❄️ Congelar Linhas")
        btn_unfreeze = QPushButton("🔥 Descongelar Linhas")
        btn_clear = QPushButton("🧹 Limpar Dados")  # Novo botão

        # define height
        btn_import.setMinimumHeight(40)
        btn_save.setMinimumHeight(40)
        btn_load.setMinimumHeight(40)
        btn_freeze.setMinimumHeight(40)
        btn_unfreeze.setMinimumHeight(40)
        btn_clear.setMinimumHeight(40)

        button_layout.addWidget(btn_import)
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_load)
        button_layout.addWidget(btn_freeze)
        button_layout.addWidget(btn_unfreeze)
        button_layout.addWidget(btn_clear)
        
        # Conecta funções
        btn_import.clicked.connect(self.import_csv)
        btn_save.clicked.connect(self.save_project)
        btn_load.clicked.connect(self.load_project)
        btn_freeze.clicked.connect(self.freeze_selected)
        btn_unfreeze.clicked.connect(self.unfreeze_selected)
        btn_clear.clicked.connect(self.clear_data)  # Conecta ao método

        # -------------------
        # Painel lateral de cálculos
        # -------------------
        self.calc_panel = QVBoxLayout()
        self.calc_panel.addWidget(QLabel("📊 Cálculos Disponíveis"))

        btn_mean = QPushButton("Média")
        btn_std = QPushButton("Desvio Padrão")
        btn_corr = QPushButton("Correlação")

        # define height
        btn_mean.setMinimumHeight(40)
        btn_std.setMinimumHeight(40)
        btn_corr.setMinimumHeight(40)

        self.calc_panel.addWidget(btn_mean)
        self.calc_panel.addWidget(btn_std)
        self.calc_panel.addWidget(btn_corr)
        self.calc_panel.addStretch()

        # Conecta funções
        btn_mean.clicked.connect(self.calculate_mean)
        btn_std.clicked.connect(self.calculate_std)
        btn_corr.clicked.connect(self.calculate_correlation)

        # Adiciona ambos layouts laterais ao layout principal
        side_panel = QVBoxLayout()
        side_panel.addLayout(button_layout)
        side_panel.addLayout(self.calc_panel)
        side_panel.addStretch()

        main_layout.addLayout(side_panel, 1)
        self.setCentralWidget(main_widget)

    # -------------------
    # Funções de cálculos
    # -------------------
    def calculate_mean(self):
        df = data_store.get_active_data()
        if df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado disponível.")
            return
        results = mo.calculate_mean(df)
        QMessageBox.information(self, "Média", str(results))

    def calculate_std(self):
        df = data_store.get_active_data()
        if df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado disponível.")
            return
        results = mo.calculate_std(df)
        QMessageBox.information(self, "Desvio Padrão", str(results))

    def calculate_correlation(self):
        df = data_store.get_active_data()
        if df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado disponível.")
            return
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) < 2:
            QMessageBox.warning(self, "Erro", "Necessário pelo menos duas colunas numéricas para correlação.")
            return
        corr = mo.calculate_correlation(df, num_cols[0], num_cols[1])
        QMessageBox.information(self, f"Correlação ({num_cols[0]} x {num_cols[1]})", f"{corr:.4f}")

    # -------------------
    # Importação / Salvar / Abrir
    # -------------------
    def import_csv(self):
        dlg = LayoutSelectorDialog()
        layout_name = dlg.get_selected_layout()
        if not layout_name:
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecione um ou mais arquivos",
            "",
            "Arquivos de dados (*.csv *.txt *.xlsx)"
        )
        if not file_paths:
            return

        try:
            df = import_files(file_paths, layout_name)
            data_store.add_data(df)
            self.table.update_table(data_store.data, data_store.frozen_rows)
            self.graph_panel.update_graph(data_store.get_active_data())
            QMessageBox.information(self, "Sucesso", f"{len(file_paths)} arquivo(s) importado(s) com layout '{layout_name}'.")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao importar", str(e))

    def save_project(self):
        data = data_store.get_data()
        if data is None or data.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado carregado para salvar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Projeto", "", "Wind Project (*.wnd)")
        if not file_path:
            return

        try:
            data.to_pickle(file_path)
            QMessageBox.information(self, "Sucesso", "Projeto salvo com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar o projeto:\n{e}")

    def load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Projeto", "", "Wind Project (*.wnd)")
        if not file_path:
            return
        try:
            df = pd.read_pickle(file_path)
            data_store.set_data(df)
            self.table.update_table(df, data_store.frozen_rows)
            self.graph_panel.update_graph(data_store.get_active_data())
            QMessageBox.information(self, "Sucesso", "Projeto carregado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o projeto:\n{e}")

    # -------------------
    # Congelar / Descongelar linhas
    # -------------------
    def freeze_selected(self):
        indices = self.table.get_selected_indices()
        data_store.freeze_rows(indices)
        self.table.update_table(data_store.data, data_store.frozen_rows)
        self.graph_panel.update_graph(data_store.get_active_data())

    def unfreeze_selected(self):
        indices = self.table.get_selected_indices()
        data_store.unfreeze_rows(indices)
        self.table.update_table(data_store.data, data_store.frozen_rows)
        self.graph_panel.update_graph(data_store.get_active_data())

    # -------------------
    # Método para limpar dados
    # -------------------
    def clear_data(self):
        reply = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja realmente limpar todos os dados importados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            data_store.data = pd.DataFrame()
            data_store.frozen_rows.clear()
            self.table.update_table(data_store.data, data_store.frozen_rows)
            self.graph_panel.update_graph(data_store.get_active_data())
            QMessageBox.information(self, "Sucesso", "Todos os dados foram limpos.")
