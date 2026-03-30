# ParliamentLens

ParliamentLens is a data analytics and dashboard project focused on exploring Canadian parliamentary activity through bills, transcripts, voting sessions, and topic-level patterns.

The project aims to turn raw parliamentary datasets into a structured analytical system that can help answer questions such as:

- Which MPs are most active in debate and legislation?
- What topics dominate parliamentary speech and bills?
- How do party agendas differ in what they say versus what they do?
- Which topics gain attention over time?
- How can speech, bills, and voting be connected in one analytical view?

## Project Goal

The main goal of ParliamentLens is to build an interactive analytics platform for parliamentary data using **Streamlit** as the primary application layer, with a smaller **Power BI** KPI layer for presentation and reporting.

This project is not just about creating charts. It is about building a reusable system for:

- understanding legislative activity
- analyzing parliamentary discourse
- tracking issue attention over time
- comparing MPs and parties
- preparing the foundation for NLP and search-based exploration later

## Why I Built This Project

I wanted to work on a project that combines:

- data cleaning and validation
- analytical thinking
- dashboard design
- political / legislative data exploration
- future NLP opportunities

The datasets already contain rich information across multiple parliamentary sources, but they are not directly ready for analysis. This project is my way of transforming them into a clear, structured, and explainable analytical workflow.

I also want this project to reflect a realistic analytics process:
- first understand the data
- then clean and validate it carefully
- then build features and dashboards
- and only after that move into more advanced text and product-style exploration

## Data Used

The project currently works with these main sources:

### Bills
Contains legislative metadata such as:
- bill name
- number
- parliament and session
- status and stage
- sponsor information
- topics
- summaries

### Transcripts
Contains parliamentary speech data such as:
- speaker name
- constituency
- party
- parliament
- time
- speech text
- level 2 and level 3 topics

There are currently two transcript versions:
- topic-only transcripts
- transcripts with speech text

### Voting Sessions
Contains parliamentary voting-related records tied to legislative context.

### Supporting Reference Data
Additional files include:
- legislators
- topics
- committees
- committee members

## Current Direction

The project is currently in the **foundation stage**.

So far, I have focused on:
- setting up the project structure
- building reusable Python modules for loading and cleaning data
- validating schemas and missing values
- checking duplicate behavior
- parsing time fields correctly
- auditing text fields before making stronger cleaning assumptions

At this stage, the focus is on building a reliable base before feature engineering and dashboard development.

## Planned Architecture

The project is being built in two layers:

### 1. Streamlit
Streamlit will be the main application layer and will contain:
- overview dashboards
- bills analysis
- transcript analysis
- topic analysis
- MP and party pages
- later, exploratory and search-style views

### 2. Power BI
Power BI will be used later as a lightweight presentation layer for:
- high-level KPIs
- executive summaries
- presentation-ready dashboards

## What I Want the Final Project to Become

My target is for ParliamentLens to evolve into a parliamentary intelligence dashboard that can support:

- descriptive analytics
- topic trend analysis
- MP and party comparison
- bill progression tracking
- speech and agenda analysis
- voting behavior analysis
- later, NLP-based text exploration

## Main Development Principles

A few principles guide the project:

- preserve raw source values whenever possible
- avoid aggressive cleaning before inspection
- keep reusable logic in Python files, not only notebooks
- separate data logic from dashboard UI
- build the project incrementally and transparently

## Current Progress

Completed so far:
- project structure
- path management
- data loaders
- safe cleaning functions
- validation helpers
- initial data audit notebook

## TODO

### Foundation and Data Preparation
- [x] Set up project structure
- [x] Create data path management
- [x] Create reusable CSV loaders
- [x] Create initial cleaning utilities
- [x] Create validation helpers
- [x] Build first data audit notebook
- [ ] Save cleaned master datasets to parquet
- [ ] Add stronger duplicate investigation for transcript data
- [ ] Finalize handling of placeholder text values
- [ ] Decide how to handle procedural / low-information transcript text

### Feature Engineering
- [ ] Create overview feature functions
- [ ] Create bill-level summary features
- [ ] Create transcript-level summary features
- [ ] Create topic-level summary features
- [ ] Create MP-level summary features
- [ ] Create party-level summary features
- [ ] Design metrics for sponsor activity and topic ownership

### Streamlit Dashboard
- [ ] Build overview page
- [ ] Build bills page
- [ ] Build transcripts page
- [ ] Build topics page
- [ ] Build MPs and parties page
- [ ] Build voting page
- [ ] Add shared filters across pages
- [ ] Add interactive charts and tables
- [ ] Improve app layout and visual consistency

### Analytical Expansion
- [ ] Compare party speech agenda vs legislative agenda
- [ ] Analyze topic trends over time
- [ ] Analyze sponsor effectiveness
- [ ] Analyze party cohesion and vote divergence
- [ ] Explore topic ownership by MP
- [ ] Link speech activity to bill and voting behavior

### NLP and Text Exploration
- [ ] Profile procedural vs substantive transcript text
- [ ] Add text-specific cleaning rules where justified
- [ ] Explore named entity extraction
- [ ] Explore framing / rhetoric analysis
- [ ] Explore tone or speech-style changes over time
- [ ] Evaluate whether semantic search is feasible

### Power BI Layer
- [ ] Export high-level KPI tables
- [ ] Build a compact Power BI presentation dashboard
- [ ] Create presentation-ready summary views

### Final Project Polish
- [ ] Improve documentation
- [ ] Add screenshots / demo images
- [ ] Add example outputs
- [ ] Refactor repeated code where needed
- [ ] Add tests for the main data modules
- [ ] Prepare final portfolio presentation of the project

## Repository Status

This repository is currently an active work in progress. The foundation layer is being built first so later analysis and dashboard features can rest on a more reliable and explainable data pipeline.

## Author

Built as a personal data analytics and dashboard project around Canadian parliamentary data.