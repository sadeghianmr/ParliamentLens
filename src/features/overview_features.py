"""
Create overview-level analytical features for the ParliamentLens dashboard.

This module transforms cleaned datasets into KPI values and grouped summary
tables that can be used directly in the Streamlit overview page.

The implementation is intentionally conservative with memory usage, especially
for large transcript datasets.
"""

from __future__ import annotations

import pandas as pd


def _safe_nunique(df: pd.DataFrame, column: str) -> int:
    """
    Return the number of unique non-null values in a column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Column name.

    Returns
    -------
    int
        Number of unique non-null values, or 0 if the column does not exist.
    """
    if column not in df.columns:
        return 0

    return int(df[column].dropna().nunique())


def _count_unique_items_in_list_column(df: pd.DataFrame, column: str) -> int:
    """
    Count unique values in a parsed list-like column.

    This uses a Series-based explode workflow to avoid copying the full dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Parsed list column.

    Returns
    -------
    int
        Number of unique non-null items in the exploded column.
    """
    if column not in df.columns:
        return 0

    series = df[column].dropna()
    if series.empty:
        return 0

    exploded = series.explode()
    if exploded.empty:
        return 0

    return int(exploded.dropna().nunique())


def _group_count(
    df: pd.DataFrame,
    group_column: str,
    count_name: str,
    sort_by: str | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Create a grouped count summary for one column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    group_column : str
        Column to group by.
    count_name : str
        Output count column name.
    sort_by : str | None, default=None
        Column to sort by. If None, uses count_name.
    ascending : bool, default=False
        Sort direction.

    Returns
    -------
    pd.DataFrame
        Grouped count summary.
    """
    if group_column not in df.columns:
        return pd.DataFrame(columns=[group_column, count_name])

    summary = df.groupby(group_column, dropna=False).size().reset_index(name=count_name)

    if sort_by is None:
        sort_by = count_name

    summary = summary.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)
    return summary


def _top_items_from_list_column(
    df: pd.DataFrame,
    column: str,
    top_n: int = 15,
    output_name: str = "item",
) -> pd.DataFrame:
    """
    Count the most common values from a parsed list-like column.

    This function avoids exploding the whole dataframe and only works on the
    selected Series.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Parsed list column.
    top_n : int, default=15
        Number of top items to return.
    output_name : str, default="item"
        Output column name for the exploded values.

    Returns
    -------
    pd.DataFrame
        Top items and their counts.
    """
    if column not in df.columns:
        return pd.DataFrame(columns=[output_name, "count"])

    series = df[column].dropna()
    if series.empty:
        return pd.DataFrame(columns=[output_name, "count"])

    exploded = series.explode()
    if exploded.empty:
        return pd.DataFrame(columns=[output_name, "count"])

    counts = exploded.value_counts(dropna=False).head(top_n).reset_index()
    counts.columns = [output_name, "count"]
    return counts


def _top_items_from_scalar_column(
    df: pd.DataFrame,
    column: str,
    top_n: int = 15,
    output_name: str = "item",
) -> pd.DataFrame:
    """
    Count the most common values from a scalar column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Scalar column.
    top_n : int, default=15
        Number of top items to return.
    output_name : str, default="item"
        Output column name.

    Returns
    -------
    pd.DataFrame
        Top items and their counts.
    """
    if column not in df.columns:
        return pd.DataFrame(columns=[output_name, "count"])

    counts = df[column].value_counts(dropna=False).head(top_n).reset_index()
    counts.columns = [output_name, "count"]
    return counts


def get_overview_kpis(
    bills_df: pd.DataFrame,
    transcripts_df: pd.DataFrame,
    voting_df: pd.DataFrame,
) -> dict:
    """
    Create headline KPI values for the overview page.

    Parameters
    ----------
    bills_df : pd.DataFrame
        Cleaned bills dataframe.
    transcripts_df : pd.DataFrame
        Cleaned transcripts dataframe.
    voting_df : pd.DataFrame
        Cleaned voting dataframe.

    Returns
    -------
    dict
        Dictionary of overview KPI values.
    """
    topic_column = None
    if "level_2_topics_list" in transcripts_df.columns:
        topic_column = "level_2_topics_list"
    elif "level_2_topics" in transcripts_df.columns:
        topic_column = "level_2_topics"

    if topic_column == "level_2_topics_list":
        unique_topics = _count_unique_items_in_list_column(transcripts_df, topic_column)
    elif topic_column is not None:
        unique_topics = _safe_nunique(transcripts_df, topic_column)
    else:
        unique_topics = 0

    return {
        "total_bills": int(len(bills_df)),
        "total_transcript_rows": int(len(transcripts_df)),
        "total_voting_rows": int(len(voting_df)),
        "unique_speakers": _safe_nunique(transcripts_df, "name"),
        "unique_sponsors": _safe_nunique(bills_df, "sponsor_name"),
        "unique_parties": _safe_nunique(transcripts_df, "party"),
        "unique_level_2_topics": unique_topics,
    }


def get_bills_by_parliament(bills_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count bills by parliament.
    """
    return _group_count(
        bills_df,
        group_column="parliament",
        count_name="bill_count",
        sort_by="parliament",
        ascending=True,
    )


def get_bills_by_stage(bills_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count bills by stage.
    """
    return _group_count(
        bills_df,
        group_column="stage",
        count_name="bill_count",
        sort_by="bill_count",
        ascending=False,
    )


def get_bills_by_status(bills_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count bills by status.
    """
    return _group_count(
        bills_df,
        group_column="status",
        count_name="bill_count",
        sort_by="bill_count",
        ascending=False,
    )


def get_transcripts_by_parliament(transcripts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count transcript rows by parliament.
    """
    return _group_count(
        transcripts_df,
        group_column="parliament",
        count_name="transcript_count",
        sort_by="parliament",
        ascending=True,
    )


def get_transcripts_by_party(transcripts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count transcript rows by party.
    """
    return _group_count(
        transcripts_df,
        group_column="party",
        count_name="transcript_count",
        sort_by="transcript_count",
        ascending=False,
    )


def get_top_level_2_topics(
    df: pd.DataFrame,
    top_n: int = 15,
    list_column: str = "level_2_topics_list",
    fallback_column: str = "level_2_topics",
) -> pd.DataFrame:
    """
    Return the most common level 2 topics.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    top_n : int, default=15
        Number of top topics to return.
    list_column : str, default="level_2_topics_list"
        Preferred parsed list column.
    fallback_column : str, default="level_2_topics"
        Fallback raw column if parsed column is unavailable.

    Returns
    -------
    pd.DataFrame
        Top level 2 topics with counts.
    """
    if list_column in df.columns:
        return _top_items_from_list_column(
            df,
            column=list_column,
            top_n=top_n,
            output_name="level_2_topic",
        )

    if fallback_column in df.columns:
        return _top_items_from_scalar_column(
            df,
            column=fallback_column,
            top_n=top_n,
            output_name="level_2_topic",
        )

    return pd.DataFrame(columns=["level_2_topic", "count"])


def get_overview_tables(
    bills_df: pd.DataFrame,
    transcripts_df: pd.DataFrame,
) -> dict:
    """
    Build the main grouped summary tables for the overview page.

    Parameters
    ----------
    bills_df : pd.DataFrame
        Cleaned bills dataframe.
    transcripts_df : pd.DataFrame
        Cleaned transcripts dataframe.

    Returns
    -------
    dict
        Dictionary of grouped summary dataframes.
    """
    return {
        "bills_by_parliament": get_bills_by_parliament(bills_df),
        "bills_by_stage": get_bills_by_stage(bills_df),
        "bills_by_status": get_bills_by_status(bills_df),
        "transcripts_by_parliament": get_transcripts_by_parliament(transcripts_df),
        "transcripts_by_party": get_transcripts_by_party(transcripts_df),
        "top_bill_topics": get_top_level_2_topics(bills_df),
        "top_transcript_topics": get_top_level_2_topics(transcripts_df),
    }