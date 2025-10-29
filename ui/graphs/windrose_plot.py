import plotly.express as px
import pandas as pd
import numpy as np

def create_windrose_plot(df: pd.DataFrame):
    # procura colunas relacionadas
    speed_col = next((c for c in df.columns if "wind" in c.lower() or "speed" in c.lower()), None)
    dir_col = next((c for c in df.columns if "dir" in c.lower()), None)

    if not speed_col or not dir_col:
        return px.scatter_polar(r=[0], theta=[0], title="Colunas de vento não encontradas")

    fig = px.bar_polar(
        df,
        r=speed_col,
        theta=dir_col,
        color=speed_col,
        color_continuous_scale="Viridis",
        title="Rosa dos Ventos 🌬️",
    )
    fig.update_layout(template="plotly_dark", height=500)
    return fig
