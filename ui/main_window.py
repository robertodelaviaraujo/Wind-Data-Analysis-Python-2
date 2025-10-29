from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QPushButton, QFileDialog, QMessageBox, QLabel
)
from ui.data_table_view import DataTableView
from ui.graph_panel import GraphPanel
from ui.dialogs.layout_selector_dialog import LayoutSelectorDialog
from core.file_importer import import_files
from core.data_store import data_store
import core.math_operations as mo
import pandas as pd
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌬️ Wind Analyzer - Software de Anemometria")
        self.resize(1400, 800)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # -------------------
        # Botões horizontais no topo
        # -------------------
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        btn_layout.setSpacing(5)

        self.btn_import = QPushButton("📂 Importar Arquivos")
        self.btn_save = QPushButton("💾 Salvar Projeto (.wnd)")
        self.btn_load = QPushButton("📁 Abrir Projeto (.wnd)")
        self.btn_freeze = QPushButton("❄️ Congelar Linhas")
        self.btn_unfreeze = QPushButton("🔥 Descongelar Linhas")
        self.btn_clear = QPushButton("🧹 Limpar Dados")

        for btn in [self.btn_import, self.btn_save, self.btn_load, self.btn_freeze, self.btn_unfreeze, self.btn_clear]:
            btn.setFixedHeight(30)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)

        # -------------------
        # Corpo principal com splitter (2 colunas ajustáveis)
        # -------------------
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Coluna 1: Tabela de dados
        self.table = DataTableView()
        splitter.addWidget(self.table)

        # Coluna 2: Painel de gráficos
        self.graph_panel = GraphPanel()
        splitter.addWidget(self.graph_panel)

        # Define proporção inicial das colunas (tabela 40%, gráficos 60%)
        splitter.setSizes([600, 800])

        main_layout.addWidget(splitter)

        # -------------------
        # Painel de cálculos abaixo dos botões
        # -------------------
        calc_layout = QHBoxLayout()
        calc_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        calc_layout.setSpacing(5)

        self.btn_mean = QPushButton("Média")
        self.btn_std = QPushButton("Desvio Padrão")
        self.btn_corr = QPushButton("Correlação")

        for btn in [self.btn_mean, self.btn_std, self.btn_corr]:
            btn.setFixedHeight(30)
            calc_layout.addWidget(btn)

        main_layout.addLayout(calc_layout)

        self.setCentralWidget(main_widget)

        # -------------------
        # Conecta funções
        # -------------------
        self.btn_import.clicked.connect(self.import_csv)
        self.btn_save.clicked.connect(self.save_project)
        self.btn_load.clicked.connect(self.load_project)
        self.btn_freeze.clicked.connect(self.freeze_selected)
        self.btn_unfreeze.clicked.connect(self.unfreeze_selected)
        self.btn_clear.clicked.connect(self.clear_data)

        self.btn_mean.clicked.connect(self.calculate_mean)
        self.btn_std.clicked.connect(self.calculate_std)
        self.btn_corr.clicked.connect(self.calculate_correlation)

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
            self.table.update_table(data_store.get_data(), data_store.frozen_rows)
            self.graph_panel.update_graphs()
            QMessageBox.information(self, "Sucesso", f"{len(file_paths)} arquivo(s) importado(s) com layout '{layout_name}'.")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao importar", str(e))

    def save_project(self):
        df = data_store.get_data()
        if df.empty:
            QMessageBox.warning(self, "Aviso", "Nenhum dado carregado para salvar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Projeto", "", "Wind Project (*.wnd)")
        if not file_path:
            return

        try:
            df.to_pickle(file_path)
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
            self.graph_panel.update_graphs()
            QMessageBox.information(self, "Sucesso", "Projeto carregado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o projeto:\n{e}")

    # -------------------
    # Congelar / Descongelar linhas
    # -------------------
    def freeze_selected(self):
        indices = self.table.get_selected_indices()
        data_store.freeze_rows(indices)
        self.table.update_table(data_store.get_data(), data_store.frozen_rows)
        self.graph_panel.update_graphs()

    def unfreeze_selected(self):
        indices = self.table.get_selected_indices()
        data_store.unfreeze_rows(indices)
        self.table.update_table(data_store.get_data(), data_store.frozen_rows)
        self.graph_panel.update_graphs()

    # -------------------
    # Limpar dados
    # -------------------
    def clear_data(self):
        reply = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja realmente limpar todos os dados importados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            data_store.set_data(pd.DataFrame())
            data_store.frozen_rows.clear()
            self.table.update_table(data_store.get_data(), data_store.frozen_rows)
            self.graph_panel.update_graphs()
            QMessageBox.information(self, "Sucesso", "Todos os dados foram limpos.")
