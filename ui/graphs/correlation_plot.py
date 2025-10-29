import plotly.express as px
import pandas as pd
import numpy as np

def create_correlation_plot(df: pd.DataFrame):
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) < 2:
        return px.imshow([[0]], text_auto=True, title="Sem colunas suficientes para correlação")

    corr = df[num_cols].corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Matriz de Correlação",
        aspect="auto"
    )
    fig.update_layout(template="plotly_dark", height=500)
    return fig
