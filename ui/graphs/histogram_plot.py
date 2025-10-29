import plotly.express as px
import pandas as pd

def create_histogram_plot(df: pd.DataFrame):
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) == 0:
        return px.histogram(x=[]).update_layout(title="Nenhuma coluna numérica encontrada")

    fig = px.histogram(df, x=num_cols[0], nbins=30, color_discrete_sequence=["skyblue"])
    fig.update_layout(title=f"Histograma de {num_cols[0]}", height=350)
    return fig
