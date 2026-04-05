# ParliamentLens

ParliamentLens is a data analytics and dashboard project for exploring Canadian parliamentary activity through bills, transcripts, voting sessions, and topic-level patterns.

The project is built around one main idea: turn raw parliamentary datasets into a structured, explainable workflow that supports both dashboarding and deeper political analysis.

## Project goal

The goal of ParliamentLens is to build an interactive parliamentary analytics platform in **Streamlit**, with a smaller **Power BI** layer later for presentation-ready KPI reporting.

The project is designed to support questions such as:

- Which MPs are most active in debate and legislation?
- What topics dominate parliamentary speech and bills?
- How do party agendas differ in what they say versus what they do?
- How does issue attention change across parliaments?
- How can speeches, bills, and votes be connected in one analytical view?

## Why I built it

I wanted a project that combines:
- data cleaning and validation
- analytical thinking
- dashboard design
- political / legislative data exploration
- future NLP opportunities

The datasets already contain a lot of useful information, but they are not immediately ready for analysis. ParliamentLens is my way of building a cleaner and more reusable system around them instead of jumping straight into charts.

## Current status

The project has moved beyond the initial data-foundation stage and into the first dashboard stage.

At the moment, the repository includes:
- reusable data loading, cleaning, and validation modules
- notebook-based data auditing
- overview KPI and grouped summary feature functions
- reusable Plotly chart helpers
- the first Streamlit app structure
- the first overview dashboard page with sidebar filters

The current focus is on improving the overview experience and then expanding into dedicated pages for bills, transcripts, topics, and voting.

## Project structure

```text
ParliamentLens/
├── app.py
├── requirements.txt
├── README.md
├── config/
│   └── theme.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_audit.ipynb
│   └── 02_overview_features.ipynb
├── pages/
│   └── 1_Overview.py
├── src/
│   ├── data/
│   ├── features/
│   └── visuals/
└── .streamlit/
    └── config.toml
```

## How the project is being built

The project is being built in layers:

1. **Data pipeline**  
   Load, clean, and validate the raw datasets.

2. **Feature layer**  
   Turn cleaned data into reusable KPIs and grouped summary tables.

3. **Chart layer**  
   Keep plotting logic separate from Streamlit pages for easier maintenance.

4. **App layer**  
   Build Streamlit pages gradually, starting from the overview page.

5. **Presentation layer later**  
   Export high-level KPI tables for a compact Power BI dashboard.

## Development principles

A few principles guide the project:

- preserve raw source values whenever possible
- avoid aggressive cleaning before inspection
- keep reusable logic in Python files, not only notebooks
- separate data logic from dashboard UI
- build incrementally and test each layer before moving on

## Roadmap

### Done
- [x] set up the project structure
- [x] build the data loading, cleaning, and validation layer
- [x] create data audit and feature testing notebooks
- [x] build overview feature functions
- [x] create reusable Plotly chart helpers
- [x] build the first Streamlit overview page

### Next
- [ ] improve and polish the overview page
- [ ] build dedicated pages for bills, transcripts, topics, and voting
- [ ] expand feature engineering for MPs, parties, and voting behavior
- [ ] explore text-specific and NLP-driven analysis
- [ ] add a compact Power BI presentation layer

## Repository status

This repository is an active work in progress. The foundation, first feature layer, reusable chart helpers, and first Streamlit page are already in place. The next step is to refine the current dashboard and expand the app page by page.

## Author

Built as a personal data analytics and dashboard project around Canadian parliamentary data.