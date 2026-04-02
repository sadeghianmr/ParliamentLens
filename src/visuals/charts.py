"""
Create reusable Plotly charts for the ParliamentLens dashboard.

This module keeps chart construction separate from Streamlit page code so the
UI layer stays focused on layout and interaction.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


DEFAULT_HEIGHT = 420


def _empty_figure(message: str = "No data available") -> go.Figure:
    """
    Return a simple placeholder figure when there is no data to plot.

    Parameters
    ----------
    message : str, default="No data available"
        Message shown in the figure.

    Returns
    -------
    go.Figure
        Plotly figure with a centered annotation.
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 16},
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        height=DEFAULT_HEIGHT,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        template="plotly_white",
    )
    return fig


def _apply_standard_layout(
    fig: go.Figure,
    title: str,
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Apply a consistent layout style to a Plotly figure.

    Parameters
    ----------
    fig : go.Figure
        Input figure.
    title : str
        Figure title.
    height : int, default=DEFAULT_HEIGHT
        Figure height.

    Returns
    -------
    go.Figure
        Styled figure.
    """
    fig.update_layout(
        title=title,
        height=height,
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        title_x=0.0,
    )
    return fig


def plot_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Create a vertical bar chart.

    Parameters
    ----------
    df : pd.DataFrame
        Input summary dataframe.
    x : str
        Column for the x-axis.
    y : str
        Column for the y-axis.
    title : str
        Chart title.
    height : int, default=DEFAULT_HEIGHT
        Figure height.

    Returns
    -------
    go.Figure
        Plotly bar chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    fig = px.bar(df, x=x, y=y)
    fig = _apply_standard_layout(fig, title=title, height=height)
    return fig


def plot_horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Create a horizontal bar chart.

    Parameters
    ----------
    df : pd.DataFrame
        Input summary dataframe.
    x : str
        Column for the x-axis.
    y : str
        Column for the y-axis.
    title : str
        Chart title.
    height : int, default=DEFAULT_HEIGHT
        Figure height.

    Returns
    -------
    go.Figure
        Plotly horizontal bar chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    fig = px.bar(df, x=x, y=y, orientation="h")
    fig = _apply_standard_layout(fig, title=title, height=height)
    return fig


def plot_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Create a line chart.

    Parameters
    ----------
    df : pd.DataFrame
        Input summary dataframe.
    x : str
        Column for the x-axis.
    y : str
        Column for the y-axis.
    title : str
        Chart title.
    height : int, default=DEFAULT_HEIGHT
        Figure height.

    Returns
    -------
    go.Figure
        Plotly line chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    fig = px.line(df, x=x, y=y, markers=True)
    fig = _apply_standard_layout(fig, title=title, height=height)
    return fig


def plot_top_topics_chart(
    df: pd.DataFrame,
    title: str,
    topic_column: str = "level_2_topic",
    count_column: str = "count",
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Create a horizontal bar chart for top topics.

    Parameters
    ----------
    df : pd.DataFrame
        Topic summary dataframe.
    title : str
        Chart title.
    topic_column : str, default="level_2_topic"
        Topic label column.
    count_column : str, default="count"
        Topic count column.
    height : int, default=DEFAULT_HEIGHT
        Figure height.

    Returns
    -------
    go.Figure
        Plotly horizontal bar chart for topics.
    """
    return plot_horizontal_bar_chart(
        df=df,
        x=count_column,
        y=topic_column,
        title=title,
        height=height,
    )