import plotly.express as px
import pandas as pd
import plotly.io as pio

def generate_heatmap(data, title, value_col, x_label='Hour', y_label='Weekday', color_scale='Blues'):
    """
    Generate a heatmap for the specified value column in the data.
    
    Parameters
    ----------
    data : pd.DataFrame
        The dataset containing the relevant columns.
    title : str
        Title of the heatmap.
    value_col : str
        Column to use for the values in the heatmap.
    x_label : str
        Label for the x-axis.
    y_label : str
        Label for the y-axis.
    color_scale : str
        Color scale for the heatmap.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The heatmap figure.
    """
    # Group the data by 'weekday' and 'hour' to remove duplicates, and calculate the mean (or sum) of the value_col
    grouped_data = data.groupby(['weekday', 'hour'])[value_col].mean().reset_index()

    # Pivot the data to create a matrix for the heatmap
    heatmap_data = grouped_data.pivot(index='weekday', columns='hour', values=value_col)
    
    # Create the heatmap
    fig = px.imshow(heatmap_data, text_auto=True, color_continuous_scale=color_scale, title=title)
    
    # Update layout
    fig.update_layout(
        width=800,
        height=600,
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    fig.update_xaxes(tickangle=-45)
    
    return fig

def plot_correlation_matrix(correlation_matrix, title="Correlation Matrix"):
    """
    Plot the correlation matrix as a heatmap.
    
    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Correlation matrix to plot.
    title : str
        Title of the heatmap.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The heatmap figure.
    """
    fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='Viridis', title=title)
    
    fig.update_layout(
        width=800,
        height=800
    )
    fig.update_xaxes(tickangle=-45)
    
    return fig