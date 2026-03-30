"""
Load raw parliamentary datasets from disk.

This module provides reusable loaders for individual CSV files and grouped
datasets such as bills, transcripts, and voting sessions. It also includes
small utilities to inspect dataframe size during development.
"""

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.data.paths import (
    BILLS_FILES,
    COMMITTEE_MEMBERS_FILE,
    COMMITTEES_FILE,
    LEGISLATORS_FILE,
    TOPICS_FILE,
    TRANSCRIPT_TEXT_FILES,
    TRANSCRIPT_TOPIC_FILES,
    VOTING_FILES,
    PARLIAMENT_LEGISLATOR_FILES,
)


def format_bytes(num_bytes: int) -> str:
    """
    Convert a byte count into a readable string.

    Parameters
    ----------
    num_bytes : int
        Number of bytes.

    Returns
    -------
    str
        Human-readable size string.
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} TB"


def dataframe_memory_usage(df: pd.DataFrame) -> int:
    """
    Return the estimated memory usage of a dataframe in bytes.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    int
        Estimated memory usage in bytes.
    """
    return int(df.memory_usage(deep=True).sum())


def print_dataframe_summary(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """
    Print a compact summary of dataframe size and shape.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    name : str, default="DataFrame"
        Display name used in the printed summary.
    """
    memory_bytes = dataframe_memory_usage(df)
    print(
        f"{name}: shape={df.shape}, "
        f"columns={len(df.columns)}, "
        f"memory={format_bytes(memory_bytes)}"
    )


def load_csv(file_path: Path, add_source_file: bool = True) -> pd.DataFrame:
    """
    Load a single CSV file into a pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.
    add_source_file : bool, default=True
        Whether to add a `source_file` column with the file name.

    Returns
    -------
    pd.DataFrame
        Loaded CSV data.
    """
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]

    if add_source_file:
        df["source_file"] = file_path.name

    return df


def load_and_concat_csvs(
    file_paths: Iterable[Path],
    dataset_name: str,
    add_source_file: bool = True,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Load multiple CSV files and concatenate them into a single DataFrame.

    Parameters
    ----------
    file_paths : Iterable[Path]
        Collection of CSV file paths to load.
    dataset_name : str
        Logical dataset name to store in a `dataset_name` column.
    add_source_file : bool, default=True
        Whether to add a `source_file` column for each loaded file.
    verbose : bool, default=False
        If True, print a small summary for each file and for the combined result.

    Returns
    -------
    pd.DataFrame
        Concatenated data from all provided files.
    """
    frames = []

    for file_path in file_paths:
        df = load_csv(file_path=file_path, add_source_file=add_source_file)
        df["dataset_name"] = dataset_name
        frames.append(df)

        if verbose:
            print_dataframe_summary(df, name=file_path.name)

    if not frames:
        return pd.DataFrame()

    combined_df = pd.concat(frames, ignore_index=True)

    if verbose:
        print_dataframe_summary(combined_df, name=f"{dataset_name} (combined)")

    return combined_df


def load_bills(verbose: bool = False) -> pd.DataFrame:
    """
    Load and combine all bills files.
    """
    return load_and_concat_csvs(BILLS_FILES, dataset_name="bills", verbose=verbose)


def load_transcripts_topic(verbose: bool = False) -> pd.DataFrame:
    """
    Load and combine all topic-only transcript files.
    """
    return load_and_concat_csvs(
        TRANSCRIPT_TOPIC_FILES,
        dataset_name="transcripts_topic",
        verbose=verbose,
    )


def load_transcripts_text(verbose: bool = False) -> pd.DataFrame:
    """
    Load and combine all transcript files that include text.
    """
    return load_and_concat_csvs(
        TRANSCRIPT_TEXT_FILES,
        dataset_name="transcripts_text",
        verbose=verbose,
    )


def load_voting_sessions(verbose: bool = False) -> pd.DataFrame:
    """
    Load and combine all voting session files.
    """
    return load_and_concat_csvs(
        VOTING_FILES,
        dataset_name="voting_sessions",
        verbose=verbose,
    )


def load_legislators(verbose: bool = False) -> pd.DataFrame:
    """
    Load the legislators reference file.
    """
    df = load_csv(LEGISLATORS_FILE)
    df["dataset_name"] = "legislators"

    if verbose:
        print_dataframe_summary(df, name="legislators")

    return df


def load_parliament_legislators(verbose: bool = False) -> pd.DataFrame:
    """
    Load and combine legislator reference files for Parliaments 42 to 44.

    These files are used as a whitelist to keep only federal parliamentary
    speakers in transcript datasets.
    """
    df = load_and_concat_csvs(
        PARLIAMENT_LEGISLATOR_FILES,
        dataset_name="parliament_legislators",
        verbose=verbose,
    )

    return df


def load_topics(verbose: bool = False) -> pd.DataFrame:
    """
    Load the topics reference file.
    """
    df = load_csv(TOPICS_FILE)
    df["dataset_name"] = "topics"

    if verbose:
        print_dataframe_summary(df, name="topics")

    return df


def load_committees(verbose: bool = False) -> pd.DataFrame:
    """
    Load the committees reference file.
    """
    df = load_csv(COMMITTEES_FILE)
    df["dataset_name"] = "committees"

    if verbose:
        print_dataframe_summary(df, name="committees")

    return df


def load_committee_members(verbose: bool = False) -> pd.DataFrame:
    """
    Load the committee members reference file.
    """
    df = load_csv(COMMITTEE_MEMBERS_FILE)
    df["dataset_name"] = "committee_members"

    if verbose:
        print_dataframe_summary(df, name="committee_members")

    return df