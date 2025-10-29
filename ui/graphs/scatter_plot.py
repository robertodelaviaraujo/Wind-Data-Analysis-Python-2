import plotly.graph_objects as go
import pandas as pd

def create_scatter_plot(df: pd.DataFrame):
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) < 2:
        return go.Figure().add_annotation(text="Não há colunas numéricas suficientes", x=0.5, y=0.5, showarrow=False)

    fig = go.Figure(
        data=go.Scatter(
            x=df[num_cols[0]],
            y=df[num_cols[1]],
            mode="markers",
            marker=dict(color=df[num_cols[0]], colorscale="Viridis", showscale=True),
            text=[f"{num_cols[0]}: {x}<br>{num_cols[1]}: {y}" for x, y in zip(df[num_cols[0]], df[num_cols[1]])],
        )
    )
    fig.update_layout(title=f"Dispersão: {num_cols[0]} x {num_cols[1]}", template="plotly_dark", height=500)
    return fig
