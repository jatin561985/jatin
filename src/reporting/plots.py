import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_equity_curve(equity_curve: pd.Series, title: str = "Equity Curve"):
    """
    Plots the equity curve using matplotlib.
    """
    plt.figure(figsize=(10, 6))
    equity_curve.plot()
    plt.title(title)
    plt.xlabel("Trade Number")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.savefig("data/equity_curve.png")
    plt.show()

def plot_heatmap(performance_matrix: pd.DataFrame, title: str = "Performance Heatmap"):
    """
    Plots a performance heatmap using Plotly.
    """
    fig = go.Figure(data=go.Heatmap(
        z=performance_matrix.values,
        x=performance_matrix.columns,
        y=performance_matrix.index,
        colorscale='Viridis'
    ))
    fig.update_layout(title=title)
    fig.write_image("data/performance_heatmap.png")
    fig.show()

if __name__ == "__main__":
    # Example usage:
    equity = pd.Series([100, 102, 101, 103, 102, 104, 103], name="Equity")
    plot_equity_curve(equity)

    # Dummy performance data for heatmap
    pnl_by_hour_day = pd.DataFrame({
        'Monday': [10, -5, 15],
        'Tuesday': [12, 8, -4],
        'Wednesday': [-6, 10, 20],
    }, index=['Hour 1', 'Hour 2', 'Hour 3'])

    plot_heatmap(pnl_by_hour_day)
