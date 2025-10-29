from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from core.importer.layouts import LAYOUTS


class LayoutSelectorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecione o Layout da Torre")
        self.setMinimumWidth(300)
        self.selected_layout = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Escolha o tipo de torre/layout:"))

        self.combo = QComboBox()
        self.combo.addItems(LAYOUTS.keys())
        # define widget height
        self.combo.setMinimumHeight(40)
        layout.addWidget(self.combo)

        btn_ok = QPushButton("Confirmar")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

        # define button height
        btn_ok.setMinimumHeight(40)

    def get_selected_layout(self):
        if self.exec():
            return self.combo.currentText()
        return None
