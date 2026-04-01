"""
Apply safe, minimal cleaning to parliamentary datasets.

This module focuses on technical cleaning steps that improve consistency for
analysis while preserving the original meaning of the source data.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd
import ast

def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim leading and trailing whitespace from string-like values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    pd.DataFrame
        Dataframe with trimmed string values.
    """
    cleaned_df = df.copy()
    object_columns = cleaned_df.select_dtypes(include=["object"]).columns

    for col in object_columns:
        cleaned_df[col] = cleaned_df[col].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    return cleaned_df


def replace_empty_strings_with_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace empty or whitespace-only strings with pandas NA values.

    This only affects truly empty text values. It does not change repeated
    placeholder phrases such as 'text does not exist' or 'summary not available'.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    pd.DataFrame
        Dataframe with empty strings replaced by pd.NA.
    """
    cleaned_df = df.copy()
    object_columns = cleaned_df.select_dtypes(include=["object"]).columns

    for col in object_columns:
        cleaned_df[col] = cleaned_df[col].apply(
            lambda value: pd.NA if isinstance(value, str) and not value.strip() else value
        )

    return cleaned_df


def add_unix_datetime_column(
    df: pd.DataFrame,
    source_column: str = "time",
    output_column: str = "time_dt",
) -> pd.DataFrame:
    """
    Parse a Unix timestamp column into a new datetime column.

    The original source column is preserved. This is useful when raw files store
    time as Unix seconds such as 1622749500.0.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    source_column : str, default="time"
        Name of the source timestamp column.
    output_column : str, default="time_dt"
        Name of the parsed datetime column to create.

    Returns
    -------
    pd.DataFrame
        Dataframe with an added datetime column when the source column exists.
    """
    cleaned_df = df.copy()

    if source_column not in cleaned_df.columns:
        return cleaned_df

    time_numeric = pd.to_numeric(cleaned_df[source_column], errors="coerce")
    cleaned_df[output_column] = pd.to_datetime(
        time_numeric,
        unit="s",
        errors="coerce",
        utc=True,
    )

    return cleaned_df


def parse_datetime_columns(
    df: pd.DataFrame,
    datetime_columns: Iterable[str],
) -> pd.DataFrame:
    """
    Parse selected columns into pandas datetime format.

    This is intended for columns that are already date-like strings, not Unix
    timestamps stored as numeric seconds.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    datetime_columns : Iterable[str]
        Column names to attempt parsing as datetimes.

    Returns
    -------
    pd.DataFrame
        Dataframe with parsed datetime columns where available.
    """
    cleaned_df = df.copy()

    for col in datetime_columns:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors="coerce")

    return cleaned_df


def clean_dataframe_basic(
    df: pd.DataFrame,
    datetime_columns: Iterable[str] | None = None,
    unix_time_columns: Iterable[str] | None = None,
    list_like_columns: Iterable[str] | None = None,
) -> pd.DataFrame:
    """
    Apply the default safe cleaning pipeline to a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    datetime_columns : Iterable[str] | None, default=None
        Columns to parse as regular datetimes.
    unix_time_columns : Iterable[str] | None, default=None
        Columns containing Unix timestamps in seconds. For each column, a new
        `<column>_dt` datetime column will be created.
    list_like_columns : Iterable[str] | None, default=None
        Columns containing list-like strings to parse into Python lists.
            For each column, a new `<column>_list` column will be created.
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """
    cleaned_df = strip_string_columns(df)
    cleaned_df = replace_empty_strings_with_na(cleaned_df)

    if datetime_columns:
        cleaned_df = parse_datetime_columns(cleaned_df, datetime_columns)

    if unix_time_columns:
        for col in unix_time_columns:
            cleaned_df = add_unix_datetime_column(
                cleaned_df,
                source_column=col,
                output_column=f"{col}_dt",
            )

    if list_like_columns:
        cleaned_df = parse_list_like_columns(cleaned_df, list_like_columns)
    return cleaned_df


def filter_transcript_parties(
    df: pd.DataFrame,
    party_column: str = "party",
    exclude_patterns: Iterable[str] | None = None,
) -> pd.DataFrame:
    """
    Remove transcript rows whose party name matches unwanted patterns.

    This is intended for transcript-specific filtering, for example excluding
    rows with party values related to British Columbia source noise.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    party_column : str, default="party"
        Name of the party column.
    exclude_patterns : Iterable[str] | None, default=None
        Case-insensitive text patterns to exclude from the party column.

    Returns
    -------
    pd.DataFrame
        Filtered dataframe.
    """
    cleaned_df = df.copy()

    if party_column not in cleaned_df.columns:
        return cleaned_df

    if exclude_patterns is None:
        exclude_patterns = ["bc", "british columbia"]

    pattern = "|".join(exclude_patterns)

    mask = cleaned_df[party_column].astype(str).str.contains(
        pattern,
        case=False,
        na=False,
        regex=True,
    )

    filtered_df = cleaned_df.loc[~mask].copy()
    return filtered_df


def parse_list_like_column(
    df: pd.DataFrame,
    source_column: str,
    output_column: str | None = None,
) -> pd.DataFrame:
    """
    Parse a list-like string column into a Python list.

    This is useful for columns stored as strings such as:
    '["topic1", "topic2"]'

    The original source column is preserved, and a new parsed column is created.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    source_column : str
        Name of the raw list-like string column.
    output_column : str | None, default=None
        Name of the parsed output column. If None, `<source_column>_list` is used.

    Returns
    -------
    pd.DataFrame
        Dataframe with the added parsed list column.
    """
    cleaned_df = df.copy()

    if source_column not in cleaned_df.columns:
        return cleaned_df

    if output_column is None:
        output_column = f"{source_column}_list"

    def _parse_value(value):
        if pd.isna(value):
            return pd.NA

        if isinstance(value, list):
            return value

        if not isinstance(value, str):
            return pd.NA

        value = value.strip()

        if not value:
            return pd.NA

        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
            return [parsed]
        except (ValueError, SyntaxError):
            return pd.NA

    cleaned_df[output_column] = cleaned_df[source_column].apply(_parse_value)
    return cleaned_df


def parse_list_like_columns(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    Parse multiple list-like string columns into companion list columns.

    For each source column, a new `<column>_list` column is created.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : Iterable[str]
        Column names to parse.

    Returns
    -------
    pd.DataFrame
        Dataframe with parsed list columns added.
    """
    cleaned_df = df.copy()

    for col in columns:
        cleaned_df = parse_list_like_column(cleaned_df, source_column=col)

    return cleaned_df


def add_placeholder_flag(
    df: pd.DataFrame,
    source_column: str,
    placeholder_values: Iterable[str],
    output_column: str | None = None,
) -> pd.DataFrame:
    """
    Add a boolean flag for rows where a column matches known placeholder values.

    The original source column is preserved.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    source_column : str
        Column to inspect.
    placeholder_values : Iterable[str]
        Exact placeholder strings to flag.
    output_column : str | None, default=None
        Name of the output flag column. If None, `<source_column>_is_placeholder`
        is used.

    Returns
    -------
    pd.DataFrame
        Dataframe with the added placeholder flag column.
    """
    cleaned_df = df.copy()

    if source_column not in cleaned_df.columns:
        return cleaned_df

    if output_column is None:
        output_column = f"{source_column}_is_placeholder"

    placeholder_set = {value.strip().lower() for value in placeholder_values}

    cleaned_df[output_column] = cleaned_df[source_column].apply(
        lambda value: isinstance(value, str)
        and value.strip().lower() in placeholder_set
    )

    return cleaned_df


def parse_vote_data_column(
    df: pd.DataFrame,
    source_column: str = "vote_data",
    output_column: str = "vote_data_list",
) -> pd.DataFrame:
    """
    Parse the vote_data column from a string representation into a Python list.

    The original source column is preserved, and a new parsed column is added.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    source_column : str, default="vote_data"
        Name of the raw vote data column.
    output_column : str, default="vote_data_list"
        Name of the parsed output column.

    Returns
    -------
    pd.DataFrame
        Dataframe with parsed vote data column added.
    """
    if source_column not in df.columns:
        return df

    def _parse_value(value):
        if pd.isna(value):
            return pd.NA

        if isinstance(value, list):
            return value

        if not isinstance(value, str):
            return pd.NA

        value = value.strip()
        if not value:
            return pd.NA

        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else pd.NA
        except (ValueError, SyntaxError):
            return pd.NA

    cleaned_df = df.copy()
    cleaned_df[output_column] = cleaned_df[source_column].apply(_parse_value)
    return cleaned_df


def expand_vote_data(
    df: pd.DataFrame,
    vote_data_column: str = "vote_data_list",
) -> pd.DataFrame:
    """
    Expand parsed vote_data into one row per MP vote.

    Session-level columns are repeated for each MP vote row.

    Parameters
    ----------
    df : pd.DataFrame
        Voting session dataframe with parsed vote data.
    vote_data_column : str, default="vote_data_list"
        Column containing parsed list-of-dicts vote data.

    Returns
    -------
    pd.DataFrame
        Long-format dataframe with one row per MP vote.
    """
    if vote_data_column not in df.columns:
        return pd.DataFrame()

    base_columns = [col for col in df.columns if col != vote_data_column]

    records = []

    for row in df.itertuples(index=False):
        row_dict = row._asdict()
        vote_items = row_dict.get(vote_data_column)

        if not isinstance(vote_items, list):
            continue

        session_data = {col: row_dict[col] for col in base_columns}

        for item in vote_items:
            if not isinstance(item, dict):
                continue

            combined = session_data.copy()
            combined.update(item)
            records.append(combined)

    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)