"""
Create reusable Plotly charts for the ParliamentLens dashboard.

This module keeps chart construction separate from Streamlit page code so the
UI layer stays focused on layout and interaction.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.theme import (
    CHART_COLOR_SEQUENCE,
    DEFAULT_CHART_HEIGHT,
    PRIMARY_BAR_COLOR,
    PRIMARY_LINE_COLOR,
)


DEFAULT_HEIGHT = DEFAULT_CHART_HEIGHT


def _empty_figure(message: str = "No data available") -> go.Figure:
    """
    Return a simple placeholder figure when there is no data to plot.
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
    """
    fig.update_layout(
        title=title,
        height=height,
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        title_x=0.0,
        legend_title_text="",
    )
    return fig


def _prepare_color_argument(
    df: pd.DataFrame,
    color: str | None,
    treat_color_as_category: bool = False,
):
    """
    Prepare the Plotly color argument without copying the dataframe.

    If treat_color_as_category is True, return a string version of the selected
    column so Plotly uses a discrete legend even when the source column is numeric.
    """
    if color is None or color not in df.columns:
        return None

    if not treat_color_as_category:
        return color

    return df[color].astype(str).rename(color)


def _validated_color_column(df: pd.DataFrame, color: str | None) -> str | None:
    """
    Return a valid color column name if it exists in the dataframe.
    """
    if color and color in df.columns:
        return color
    return None


def _apply_axis_types(
    fig: go.Figure,
    treat_x_as_category: bool = False,
    treat_y_as_category: bool = False,
) -> go.Figure:
    """
    Force selected axes to behave as categorical axes.
    """
    if treat_x_as_category:
        fig.update_xaxes(type="category")

    if treat_y_as_category:
        fig.update_yaxes(type="category")

    return fig


def plot_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    height: int = DEFAULT_HEIGHT,
    barmode: str = "group",
    treat_x_as_category: bool = False,
    treat_y_as_category: bool = False,
    treat_color_as_category: bool = False,
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
    color : str | None, default=None
        Optional column used to color bars by unique values.
    height : int, default=DEFAULT_HEIGHT
        Figure height.
    barmode : str, default="group"
        Plotly bar mode. Common options are "group", "stack", and "relative".
    treat_x_as_category : bool, default=False
        Force the x-axis to behave as categorical.
    treat_y_as_category : bool, default=False
        Force the y-axis to behave as categorical.
    treat_color_as_category : bool, default=False
        Force the color grouping to behave as categorical, which can be helpful when the source column is numeric but should be treated as discrete groups.

    Returns
    -------
    go.Figure
        Plotly bar chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    color = _prepare_color_argument(
        df,
        color=color,
        treat_color_as_category=treat_color_as_category,
    )

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode=barmode,
        color_discrete_sequence=CHART_COLOR_SEQUENCE,
    )

    if color is None:
        fig.update_traces(marker_color=PRIMARY_BAR_COLOR)

    fig = _apply_standard_layout(fig, title=title, height=height)
    fig = _apply_axis_types(
        fig,
        treat_x_as_category=treat_x_as_category,
        treat_y_as_category=treat_y_as_category,
    )
    return fig


def plot_horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    height: int = DEFAULT_HEIGHT,
    barmode: str = "group",
    treat_x_as_category: bool = False,
    treat_y_as_category: bool = False,
    treat_color_as_category: bool = False,
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
    color : str | None, default=None
        Optional column used to color bars by unique values.
    height : int, default=DEFAULT_HEIGHT
        Figure height.
    barmode : str, default="group"
        Plotly bar mode. Common options are "group", "stack", and "relative".
    treat_x_as_category : bool, default=False
        Force the x-axis to behave as categorical.
    treat_y_as_category : bool, default=False
        Force the y-axis to behave as categorical.
    treat_color_as_category : bool, default=False
        Force the color grouping to behave as categorical, which can be helpful when the source column is numeric but should be treated as discrete groups.
    Returns
    -------
    go.Figure
        Plotly horizontal bar chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    color = _prepare_color_argument(
        df,
        color=color,
        treat_color_as_category=treat_color_as_category,
    )

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation="h",
        barmode=barmode,
        color_discrete_sequence=CHART_COLOR_SEQUENCE,
    )

    if color is None:
        fig.update_traces(marker_color=PRIMARY_BAR_COLOR)

    fig = _apply_standard_layout(fig, title=title, height=height)
    fig = _apply_axis_types(
        fig,
        treat_x_as_category=treat_x_as_category,
        treat_y_as_category=treat_y_as_category,
    )
    return fig


def plot_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    height: int = DEFAULT_HEIGHT,
    treat_x_as_category: bool = False,
    treat_y_as_category: bool = False,
    treat_color_as_category: bool = False,
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
    color : str | None, default=None
        Optional column used to split lines by unique values.
    height : int, default=DEFAULT_HEIGHT
        Figure height.
    treat_x_as_category : bool, default=False
        Force the x-axis to behave as categorical.
    treat_y_as_category : bool, default=False
        Force the y-axis to behave as categorical.
    treat_color_as_category : bool, default=False
        Force the color grouping to behave as categorical, which can be helpful when the source column is numeric but should be treated as discrete groups.
    Returns
    -------
    go.Figure
        Plotly line chart.
    """
    if df.empty or x not in df.columns or y not in df.columns:
        return _empty_figure()

    color = _prepare_color_argument(
        df,
        color=color,
        treat_color_as_category=treat_color_as_category,
    )

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        color_discrete_sequence=CHART_COLOR_SEQUENCE,
    )

    if color is None:
        fig.update_traces(line_color=PRIMARY_LINE_COLOR)

    fig = _apply_standard_layout(fig, title=title, height=height)
    fig = _apply_axis_types(
        fig,
        treat_x_as_category=treat_x_as_category,
        treat_y_as_category=treat_y_as_category,
    )
    return fig


def plot_top_topics_chart(
    df: pd.DataFrame,
    title: str,
    topic_column: str = "level_2_topic",
    count_column: str = "count",
    color: str | None = None,
    height: int = DEFAULT_HEIGHT,
    barmode: str = "group",
    treat_x_as_category: bool = False,
    treat_y_as_category: bool = False,
    treat_color_as_category: bool = False,
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
    color : str | None, default=None
        Optional column used to color bars by unique values.
    height : int, default=DEFAULT_HEIGHT
        Figure height.
    barmode : str, default="group"
        Plotly bar mode. Common options are "group", "stack", and "relative".
    treat_x_as_category : bool, default=False
        Force the x-axis to behave as categorical.
    treat_y_as_category : bool, default=False
        Force the y-axis to behave as categorical.

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
        color=color,
        height=height,
        barmode=barmode,
        treat_x_as_category=treat_x_as_category,
        treat_y_as_category=treat_y_as_category,
        treat_color_as_category=treat_color_as_category,
    )