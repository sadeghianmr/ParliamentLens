"""
Define all important file and folder paths for the ParliamentLens project.

This module centralizes path management so other parts of the codebase
can load data without hardcoding file locations.
"""

from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Main data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Raw data subdirectories
API_CSVS_DIR = RAW_DATA_DIR / "API_CSVs"
BILLS_DIR = RAW_DATA_DIR / "bills"
TRANSCRIPTS_DIR = RAW_DATA_DIR / "transcripts"
TRANSCRIPTS_TOPIC_DIR = TRANSCRIPTS_DIR / "topic_only"
TRANSCRIPTS_TEXT_DIR = TRANSCRIPTS_DIR / "with_text"
VOTING_DIR = RAW_DATA_DIR / "voting_sessions"
PARLIAMENT_LEGISLATORS_DIR = RAW_DATA_DIR / "legislators_by_parliament"

# API CSV files
# These are general reference files from the API export.
COMMITTEE_MEMBERS_FILE = API_CSVS_DIR / "committee_members.csv"
COMMITTEES_FILE = API_CSVS_DIR / "committees.csv"
LEGISLATORS_FILE = API_CSVS_DIR / "legislators.csv"
TOPICS_FILE = API_CSVS_DIR / "topics.csv"

# Bills files
BILLS_42_43_FILE = BILLS_DIR / "ca_fed_bills_42-43.csv"
BILLS_44_FILE = BILLS_DIR / "ca_fed_bills_44.csv"

# Transcript topic-only files
TRANSCRIPTS_42_TOPIC_FILE = TRANSCRIPTS_TOPIC_DIR / "transcripts_42_parliament.csv"
TRANSCRIPTS_43_TOPIC_FILE = TRANSCRIPTS_TOPIC_DIR / "transcripts_43_parliament.csv"
TRANSCRIPTS_44_TOPIC_FILE = TRANSCRIPTS_TOPIC_DIR / "transcripts_44_parliament.csv"

# Transcript text files
TRANSCRIPTS_43_TEXT_FILE = TRANSCRIPTS_TEXT_DIR / "transcript_43_with_text.csv"
TRANSCRIPTS_44_TEXT_FILE = TRANSCRIPTS_TEXT_DIR / "transcript_44_with_text.csv"

# Voting files
VOTING_42_43_FILE = VOTING_DIR / "ca_fed_house_vote_session_42-43.csv"
VOTING_44_FILE = VOTING_DIR / "ca_fed_house_vote_session_44.csv"

# Parliament legislator files
# These are the main whitelist files for filtering transcript rows to federal MPs.
LEGISLATORS_42_FILE = PARLIAMENT_LEGISLATORS_DIR / "legislators_42.csv"
LEGISLATORS_43_FILE = PARLIAMENT_LEGISLATORS_DIR / "legislators_43.csv"
LEGISLATORS_44_FILE = PARLIAMENT_LEGISLATORS_DIR / "legislators_44.csv"

# Grouped file collections for easier loading
BILLS_FILES = [
    BILLS_42_43_FILE,
    BILLS_44_FILE,
]

TRANSCRIPT_TOPIC_FILES = [
    TRANSCRIPTS_42_TOPIC_FILE,
    TRANSCRIPTS_43_TOPIC_FILE,
    TRANSCRIPTS_44_TOPIC_FILE,
]

TRANSCRIPT_TEXT_FILES = [
    TRANSCRIPTS_43_TEXT_FILE,
    TRANSCRIPTS_44_TEXT_FILE,
]

VOTING_FILES = [
    VOTING_42_43_FILE,
    VOTING_44_FILE,
]

PARLIAMENT_LEGISLATOR_FILES = [
    LEGISLATORS_42_FILE,
    LEGISLATORS_43_FILE,
    LEGISLATORS_44_FILE,
]

# Processed output files
BILLS_MASTER_FILE = PROCESSED_DATA_DIR / "bills_master.parquet"
TRANSCRIPTS_TOPIC_MASTER_FILE = PROCESSED_DATA_DIR / "transcripts_topic_master.parquet"
TRANSCRIPTS_TEXT_MASTER_FILE = PROCESSED_DATA_DIR / "transcripts_text_master.parquet"
VOTING_MASTER_FILE = PROCESSED_DATA_DIR / "voting_master.parquet"

# Keep both for now because they represent different sources and may serve different uses.
API_LEGISLATORS_MASTER_FILE = PROCESSED_DATA_DIR / "api_legislators_master.parquet"
PARLIAMENT_LEGISLATORS_MASTER_FILE = PROCESSED_DATA_DIR / "parliament_legislators_master.parquet"

TOPICS_MASTER_FILE = PROCESSED_DATA_DIR / "topics_master.parquet"