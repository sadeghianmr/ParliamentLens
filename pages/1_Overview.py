"""
Render the main overview page for ParliamentLens.

This page connects the cleaned datasets, overview feature functions, and
reusable chart helpers into the first Streamlit dashboard view.
"""

from __future__ import annotations

import streamlit as st

from src.data.loader import (
    load_bills,
    load_transcripts_text,
    load_voting_sessions,
)
from src.data.cleaning import (
    clean_dataframe_basic,
    filter_transcript_parties,
)
from src.features.overview_features import (
    get_overview_kpis,
    get_overview_tables,
)
from src.visuals.charts import (
    plot_bar_chart,
    plot_horizontal_bar_chart,
    plot_top_topics_chart,
)


st.set_page_config(
    page_title="Overview | ParliamentLens",
    page_icon="📊",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_overview_data():
    """
    Load and clean the datasets needed for the overview page.

    Returns
    -------
    tuple
        Cleaned bills, transcripts, and voting dataframes.
    """
    bills_df = load_bills(verbose=False)
    transcripts_text_df = load_transcripts_text(verbose=False)
    voting_df = load_voting_sessions(verbose=False)

    bills_clean = clean_dataframe_basic(
        bills_df,
        list_like_columns=["topics", "level_2_topics"],
    )

    transcripts_clean = clean_dataframe_basic(
        transcripts_text_df,
        unix_time_columns=["time"],
        list_like_columns=["level_2_topics", "level_3_topics"],
    )
    transcripts_clean = filter_transcript_parties(transcripts_clean)

    voting_clean = clean_dataframe_basic(
        voting_df,
        datetime_columns=["date"],
    )

    return bills_clean, transcripts_clean, voting_clean


def get_filter_options(
    bills_df,
    transcripts_df,
    voting_df,
):
    """
    Build sidebar filter options from the cleaned datasets.
    """
    parliament_values = set()

    if "parliament" in bills_df.columns:
        parliament_values.update(bills_df["parliament"].dropna().unique().tolist())

    if "parliament" in transcripts_df.columns:
        parliament_values.update(transcripts_df["parliament"].dropna().unique().tolist())

    if "parliament" in voting_df.columns:
        parliament_values.update(voting_df["parliament"].dropna().unique().tolist())

    parliaments = sorted(parliament_values)

    parties = []
    if "party" in transcripts_df.columns:
        parties = sorted(transcripts_df["party"].dropna().unique().tolist())

    return parliaments, parties


def apply_overview_filters(
    bills_df,
    transcripts_df,
    voting_df,
    selected_parliaments,
    selected_parties,
):
    """
    Apply sidebar filters to the overview datasets.

    Parameters
    ----------
    bills_df : pd.DataFrame
        Cleaned bills dataframe.
    transcripts_df : pd.DataFrame
        Cleaned transcript dataframe.
    voting_df : pd.DataFrame
        Cleaned voting dataframe.
    selected_parliaments : list
        Selected parliament values.
    selected_parties : list
        Selected party values.

    Returns
    -------
    tuple
        Filtered bills, transcripts, and voting dataframes.
    """
    if selected_parliaments:
        if "parliament" in bills_df.columns:
            bills_df = bills_df[bills_df["parliament"].isin(selected_parliaments)]

        if "parliament" in transcripts_df.columns:
            transcripts_df = transcripts_df[transcripts_df["parliament"].isin(selected_parliaments)]

        if "parliament" in voting_df.columns:
            voting_df = voting_df[voting_df["parliament"].isin(selected_parliaments)]

    if selected_parties and "party" in transcripts_df.columns:
        transcripts_df = transcripts_df[transcripts_df["party"].isin(selected_parties)]

    return bills_df, transcripts_df, voting_df


def render_sidebar_filters(
    bills_df,
    transcripts_df,
    voting_df,
):
    """
    Render the sidebar filters and return the selected values.
    """
    st.sidebar.header("Filters")

    parliaments, parties = get_filter_options(
        bills_df=bills_df,
        transcripts_df=transcripts_df,
        voting_df=voting_df,
    )

    selected_parliaments = st.sidebar.multiselect(
        "Parliament",
        options=parliaments,
        default=parliaments,
    )

    selected_parties = st.sidebar.multiselect(
        "Transcript party",
        options=parties,
        default=parties,
    )

    return selected_parliaments, selected_parties


def render_kpi_row(kpis: dict) -> None:
    """
    Render the KPI cards for the overview page.
    """
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7 = st.columns(3)

    col1.metric("Bills", f"{kpis['total_bills']:,}")
    col2.metric("Transcript records", f"{kpis['total_transcript_rows']:,}")
    col3.metric("Voting records", f"{kpis['total_voting_rows']:,}")
    col4.metric("Unique speakers", f"{kpis['unique_speakers']:,}")

    col5.metric("Unique sponsors", f"{kpis['unique_sponsors']:,}")
    col6.metric("Unique parties", f"{kpis['unique_parties']:,}")
    col7.metric("Level 2 topics", f"{kpis['unique_level_2_topics']:,}")


def main() -> None:
    """
    Render the full overview page.
    """
    st.title("ParliamentLens")
    st.caption(
        "Overview of bills, transcripts, voting records, and topic patterns "
        "across the current parliamentary datasets."
    )

    with st.spinner("Loading overview data..."):
        bills_clean, transcripts_clean, voting_clean = load_overview_data()

    selected_parliaments, selected_parties = render_sidebar_filters(
        bills_df=bills_clean,
        transcripts_df=transcripts_clean,
        voting_df=voting_clean,
    )

    bills_filtered, transcripts_filtered, voting_filtered = apply_overview_filters(
        bills_df=bills_clean,
        transcripts_df=transcripts_clean,
        voting_df=voting_clean,
        selected_parliaments=selected_parliaments,
        selected_parties=selected_parties,
    )

    overview_kpis = get_overview_kpis(
        bills_df=bills_filtered,
        transcripts_df=transcripts_filtered,
        voting_df=voting_filtered,
    )

    overview_tables = get_overview_tables(
        bills_df=bills_filtered,
        transcripts_df=transcripts_filtered,
    )

    st.subheader("Overview")
    render_kpi_row(overview_kpis)

    st.markdown("---")

    st.subheader("Legislative activity")
    col1, col2 = st.columns(2)

    with col1:
        fig_bills_by_parliament = plot_bar_chart(
            overview_tables["bills_by_parliament"],
            x="parliament",
            y="bill_count",
            title="Bills by parliament",
            treat_x_as_category=True,
        )
        st.plotly_chart(fig_bills_by_parliament, use_container_width=True)

    with col2:
        fig_bills_by_stage = plot_horizontal_bar_chart(
            overview_tables["bills_by_stage"].head(15),
            x="bill_count",
            y="stage",
            title="Bills by stage",
        )
        st.plotly_chart(fig_bills_by_stage, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_bills_by_status = plot_horizontal_bar_chart(
            overview_tables["bills_by_status"].head(15),
            x="bill_count",
            y="status",
            title="Bills by status",
        )
        st.plotly_chart(fig_bills_by_status, use_container_width=True)

    with col4:
        fig_bill_topics = plot_top_topics_chart(
            overview_tables["top_bill_topics"].head(15),
            title="Top bill topics",
        )
        st.plotly_chart(fig_bill_topics, use_container_width=True)

    st.markdown("---")

    st.subheader("Transcript activity")
    col5, col6 = st.columns(2)

    with col5:
        fig_transcripts_by_parliament = plot_bar_chart(
            overview_tables["transcripts_by_parliament"],
            x="parliament",
            y="transcript_count",
            title="Transcript records by parliament",
            treat_x_as_category=True,
        )
        st.plotly_chart(fig_transcripts_by_parliament, use_container_width=True)

    with col6:
        fig_transcripts_by_party = plot_horizontal_bar_chart(
            overview_tables["transcripts_by_party"].head(15),
            x="transcript_count",
            y="party",
            title="Transcript records by party",
        )
        st.plotly_chart(fig_transcripts_by_party, use_container_width=True)

    st.subheader("Topic activity")
    fig_transcript_topics = plot_top_topics_chart(
        overview_tables["top_transcript_topics"].head(15),
        title="Top transcript topics",
    )
    st.plotly_chart(fig_transcript_topics, use_container_width=True)

    with st.expander("Show overview tables"):
        st.markdown("#### Bills by parliament")
        st.dataframe(overview_tables["bills_by_parliament"], use_container_width=True)

        st.markdown("#### Bills by stage")
        st.dataframe(overview_tables["bills_by_stage"], use_container_width=True)

        st.markdown("#### Bills by status")
        st.dataframe(overview_tables["bills_by_status"], use_container_width=True)

        st.markdown("#### Transcript records by parliament")
        st.dataframe(overview_tables["transcripts_by_parliament"], use_container_width=True)

        st.markdown("#### Transcript records by party")
        st.dataframe(overview_tables["transcripts_by_party"], use_container_width=True)

        st.markdown("#### Top bill topics")
        st.dataframe(overview_tables["top_bill_topics"], use_container_width=True)

        st.markdown("#### Top transcript topics")
        st.dataframe(overview_tables["top_transcript_topics"], use_container_width=True)


if __name__ == "__main__":
    main()