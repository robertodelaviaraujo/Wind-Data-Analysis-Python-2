from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from ui.graphs.scatter_plot import create_scatter_plot
from ui.graphs.histogram_plot import create_histogram_plot
from ui.graphs.correlation_plot import create_correlation_plot
from ui.graphs.windrose_plot import create_windrose_plot
from core.data_store import data_store
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

    # ---------------------------
    # Atualiza todos os gráficos
    # ---------------------------
    def update_graphs(self):
        df_original = data_store.get_data()
        df_filtered = data_store.get_active_data()

        if df_original.empty:
            html = "<h3 style='text-align:center;margin-top:100px'>Nenhum dado carregado</h3>"
            for view in [self.scatter_view, self.hist_view, self.corr_view, self.windrose_view]:
                view.setHtml(html)
            return

        # Cria HTML para cada aba
        scatter_html = self._create_dual_plot_html(df_original, df_filtered, create_scatter_plot)
        hist_html = self._create_dual_plot_html(df_original, df_filtered, create_histogram_plot)
        corr_html = self._create_dual_plot_html(df_original, df_filtered, create_correlation_plot)
        wind_html = self._create_dual_plot_html(df_original, df_filtered, create_windrose_plot)

        # Exibe nos webviews
        self.scatter_view.setHtml(scatter_html)
        self.hist_view.setHtml(hist_html)
        self.corr_view.setHtml(corr_html)
        self.windrose_view.setHtml(wind_html)

    # ---------------------------
    # Função auxiliar: cria layout 2x1 (vertical)
    # ---------------------------
    def _create_dual_plot_html(self, df_original, df_filtered, plot_func):
        """Renderiza dois gráficos empilhados (originais e filtrados)."""
        fig_orig = plot_func(df_original)
        fig_filt = plot_func(df_filtered) if not df_filtered.empty else None

        html_orig = pio.to_html(fig_orig, full_html=False, include_plotlyjs='cdn')
        html_filt = (
            pio.to_html(fig_filt, full_html=False, include_plotlyjs=False)
            if fig_filt else "<div style='text-align:center;margin-top:20px;'>Sem dados filtrados</div>"
        )

        # Layout vertical
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 10px;
                    background-color: #fafafa;
                }}                
                .container {{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }}
                .chart-box {{
                    width: 100%;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    padding: 10px;
                }}
                .chart-title {{
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #333;
                }}
            </style>
        </head>
        <body>            
            <div class="container">
                <div class="chart-box">
                    <div class="chart-title">📈 Dados Originais</div>
                    {html_orig}
                </div>
                <div class="chart-box">
                    <div class="chart-title">🎯 Dados Filtrados</div>
                    {html_filt}
                </div>
            </div>
        </body>
        </html>
        """
        return html
