import plotly.express as px
import pandas as pd

def create_time_series_plot(df: pd.DataFrame):
    """Cria gráfico de série temporal (datetime x Spd_2m)."""
    if df is None or df.empty:
        return px.line(title="Nenhum dado disponível")

    if "datetime" not in df.columns or "Spd_2m" not in df.columns:
        return px.line(title="Colunas 'datetime' e/ou 'Spd_2m' não encontradas")

    # Garante que o campo datetime é datetime real
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    fig = px.line(
        df,
        x="datetime",
        y="Spd_2m",
        title="Série Temporal da Velocidade do Vento (Spd_2m)",
        color_discrete_sequence=["#007bff"],
    )

    fig.update_layout(
        height=350,
        xaxis_title="Data e Hora",
        yaxis_title="Velocidade do Vento (m/s)",
        margin=dict(l=40, r=20, t=60, b=40),
    )

    return fig
