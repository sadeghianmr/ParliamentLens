"""
Profile and validate parliamentary datasets.

This module provides lightweight inspection helpers to understand dataframe
structure, missingness, duplicate rows, repeated values, and parsed datetime
quality before adding more advanced cleaning rules.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def _make_hashable(value):
    """
    Recursively convert nested Python objects into hashable equivalents.

    Lists become tuples, and dictionaries become sorted tuples of key/value pairs.
    """
    if isinstance(value, list):
        return tuple(_make_hashable(item) for item in value)

    if isinstance(value, dict):
        return tuple(sorted((key, _make_hashable(val)) for key, val in value.items()))

    return value


def make_dataframe_hashable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of the dataframe with nested unhashable values converted
    into hashable equivalents.

    This is useful for operations like duplicated() that require hashable values.
    The original dataframe is not modified.
    """
    hashable_df = df.copy()

    for col in hashable_df.columns:
        hashable_df[col] = hashable_df[col].apply(_make_hashable)

    return hashable_df


def summarize_dataframe(df: pd.DataFrame, name: str = "DataFrame") -> pd.DataFrame:
    """
    Return a compact dataframe-level summary.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    name : str, default="DataFrame"
        Display name for the dataset.

    Returns
    -------
    pd.DataFrame
        One-row summary with shape and duplicate counts.
    """
    hashable_df = make_dataframe_hashable(df)

    summary = pd.DataFrame(
        {
            "dataset": [name],
            "rows": [len(df)],
            "columns": [len(df.columns)],
            "duplicate_rows": [int(hashable_df.duplicated().sum())],
        }
    )
    return summary


def missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize missing values by column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    pd.DataFrame
        Missing value counts and percentages by column.
    """
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2) if len(df) else 0

    summary = pd.DataFrame(
        {
            "column": missing_count.index,
            "missing_count": missing_count.values,
            "missing_pct": missing_pct.values if hasattr(missing_pct, "values") else missing_pct,
        }
    )

    summary = summary.sort_values(
        by=["missing_count", "column"],
        ascending=[False, True],
    ).reset_index(drop=True)

    return summary


def duplicate_summary(df: pd.DataFrame, subset: Iterable[str] | None = None) -> dict:
    """
    Return duplicate row counts for a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    subset : Iterable[str] | None, default=None
        Optional subset of columns used to define duplicates.

    Returns
    -------
    dict
        Duplicate count information.
    """
    hashable_df = make_dataframe_hashable(df)

    duplicate_count = int(hashable_df.duplicated(subset=subset).sum())
    total_rows = len(df)

    return {
        "total_rows": total_rows,
        "duplicate_rows": duplicate_count,
        "duplicate_pct": round((duplicate_count / total_rows * 100), 2) if total_rows else 0.0,
    }


def value_counts_summary(
    df: pd.DataFrame,
    column: str,
    top_n: int = 20,
    dropna: bool = False,
) -> pd.DataFrame:
    """
    Return the most common values in a selected column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Column to inspect.
    top_n : int, default=20
        Number of top values to return.
    dropna : bool, default=False
        Whether to exclude missing values from the counts.

    Returns
    -------
    pd.DataFrame
        Top value counts for the selected column.
    """
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "count"])

    counts = df[column].value_counts(dropna=dropna).head(top_n).reset_index()
    counts.columns = [column, "count"]
    return counts


def text_value_profile(
    df: pd.DataFrame,
    column: str,
    top_n: int = 30,
    max_length: int | None = 100,
) -> pd.DataFrame:
    """
    Profile repeated values in a text column.

    This is useful for detecting placeholder-like repeated text values before
    deciding whether any special cleaning rule is needed.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Text column to inspect.
    top_n : int, default=30
        Number of repeated values to return.
    max_length : int | None, default=100
        Optional maximum string length to keep in the output. Useful for focusing
        on short repeated phrases rather than long free text.

    Returns
    -------
    pd.DataFrame
        Repeated text values with counts and string lengths.
    """
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "count", "text_length"])

    series = df[column].dropna()

    if max_length is not None:
        series = series[series.astype(str).str.len() <= max_length]

    counts = series.value_counts().head(top_n).reset_index()
    counts.columns = [column, "count"]
    counts["text_length"] = counts[column].astype(str).str.len()

    return counts


def datetime_parse_summary(
    df: pd.DataFrame,
    source_column: str,
    parsed_column: str,
) -> dict:
    """
    Summarize the result of parsing a datetime column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    source_column : str
        Original raw time column.
    parsed_column : str
        Parsed datetime column.

    Returns
    -------
    dict
        Summary of parsing completeness and null counts.
    """
    if source_column not in df.columns or parsed_column not in df.columns:
        return {
            "source_column_exists": source_column in df.columns,
            "parsed_column_exists": parsed_column in df.columns,
            "non_null_source": None,
            "non_null_parsed": None,
            "parse_success_pct": None,
        }

    non_null_source = int(df[source_column].notna().sum())
    non_null_parsed = int(df[parsed_column].notna().sum())

    parse_success_pct = (
        round((non_null_parsed / non_null_source) * 100, 2)
        if non_null_source
        else 0.0
    )

    return {
        "source_column_exists": True,
        "parsed_column_exists": True,
        "non_null_source": non_null_source,
        "non_null_parsed": non_null_parsed,
        "parse_success_pct": parse_success_pct,
    }