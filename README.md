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
- exploring bill and voting behavior
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

At the moment, the voting data is handled mainly at the session level, but it also contains nested MP-level vote data that can later support:
- vote alignment analysis
- abstention analysis
- party cohesion analysis
- MP-level voting profiles

### Supporting Reference Data
Additional files include:
- legislators
- topics
- committees
- committee members

## Current Direction

The project is currently moving from the **foundation stage** into the **first dashboard layer**.

So far, I have focused on:
- setting up the project structure
- building reusable Python modules for loading and cleaning data
- validating schemas, missing values, and duplicate behavior
- parsing timestamps and list-like columns safely
- handling nested voting payloads for later MP-level analysis
- building the first overview feature layer
- testing grouped outputs and chart behavior in notebooks
- creating reusable Plotly chart helpers for the first dashboard page

At this stage, the focus is on turning the cleaned data pipeline into reusable dashboard components for the first Streamlit page.

## Planned Architecture

The project is being built in two layers:

### 1. Streamlit
Streamlit is the main application layer and is being built from the bottom up:
- overview metrics
- reusable chart helpers
- first overview page
- later bills, transcripts, topics, MPs, parties, and voting pages
- later exploratory and search-style views

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

## What Is Implemented Right Now

At the moment, the repository includes:
- reusable data loading, cleaning, and validation modules
- notebook-based data auditing
- overview KPI and grouped summary feature functions
- reusable Plotly chart helpers
- testing notebooks for both features and charts

The first Streamlit overview page is the next major step.

## Current Progress

Completed so far:
- project structure
- path management
- data loaders
- safe cleaning functions
- validation helpers
- initial data audit notebook
- overview feature functions
- reusable Plotly chart helpers
- overview feature testing notebook
- chart testing for grouped and colorized outputs

## TODO

### Foundation and Data Preparation
- [x] Set up project structure
- [x] Create data path management
- [x] Create reusable CSV loaders
- [x] Create initial cleaning utilities
- [x] Create validation helpers
- [x] Build first data audit notebook
- [x] Parse list-like topic columns
- [x] Add transcript party filtering for unwanted source noise
- [x] Add support for nested voting payload parsing
- [ ] Save cleaned master datasets to parquet
- [ ] Add stronger duplicate investigation for transcript data
- [ ] Finalize handling of placeholder text values
- [ ] Decide how to handle procedural / low-information transcript text
- [ ] Decide when to expand session-level voting data into MP-level vote records

### Feature Engineering
- [x] Create overview feature functions
- [ ] Create bill-level summary features
- [ ] Create transcript-level summary features
- [ ] Create topic-level summary features
- [ ] Create MP-level summary features
- [ ] Create party-level summary features
- [ ] Create voting-level summary features
- [ ] Design metrics for sponsor activity and topic ownership

### Streamlit Dashboard
- [x] Create reusable chart helpers for the overview page
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
- [ ] Explore MP-level voting analysis from nested vote session data

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

This repository is currently an active work in progress. The data foundation and first feature layer are in place, and the next step is to build the first Streamlit overview page on top of them.

## Author

Built as a personal data analytics and dashboard project around Canadian parliamentary data.