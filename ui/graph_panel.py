from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from ui.graphs.scatter_plot import create_scatter_plot
from ui.graphs.histogram_plot import create_histogram_plot
from ui.graphs.correlation_plot import create_correlation_plot
from ui.graphs.windrose_plot import create_windrose_plot
import pandas as pd
import plotly.io as pio

class GraphPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("📊 Gráficos Interativos"))

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Cria abas com webviews
        self.scatter_view = QWebEngineView()
        self.hist_view = QWebEngineView()
        self.corr_view = QWebEngineView()
        self.windrose_view = QWebEngineView()

        self.tabs.addTab(self.scatter_view, "Dispersão")
        self.tabs.addTab(self.hist_view, "Histograma")
        self.tabs.addTab(self.corr_view, "Correlação")
        self.tabs.addTab(self.windrose_view, "Rosa dos Ventos")

    def update_graph(self, df: pd.DataFrame):
        if df is None or df.empty:
            html = "<h3 style='text-align:center;margin-top:100px'>Nenhum dado carregado</h3>"
            for view in [self.scatter_view, self.hist_view, self.corr_view, self.windrose_view]:
                view.setHtml(html)
            return

        # Cada função retorna um objeto Plotly Figure
        fig_scatter = create_scatter_plot(df)
        fig_hist = create_histogram_plot(df)
        fig_corr = create_correlation_plot(df)
        fig_windrose = create_windrose_plot(df)

        # Renderiza como HTML (com PlotlyJS incluso)
        self.scatter_view.setHtml(pio.to_html(fig_scatter, full_html=False, include_plotlyjs="cdn"))
        self.hist_view.setHtml(pio.to_html(fig_hist, full_html=False, include_plotlyjs="cdn"))
        self.corr_view.setHtml(pio.to_html(fig_corr, full_html=False, include_plotlyjs="cdn"))
        self.windrose_view.setHtml(pio.to_html(fig_windrose, full_html=False, include_plotlyjs="cdn"))
