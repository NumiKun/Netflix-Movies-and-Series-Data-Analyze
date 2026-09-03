# Netflix Movies and TV Shows Data Analytics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visuals-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end data analytics portfolio project featuring an in-depth Exploratory Data Analysis (EDA) pipeline and a production-grade interactive Streamlit web dashboard analyzing Netflix's global content library up to late 2021.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset Summary](#dataset-summary)
- [Project Architecture](#project-architecture)
- [Data Preprocessing Pipeline](#data-preprocessing-pipeline)
- [Key Insights and Findings](#key-insights-and-findings)
- [Interactive Streamlit Dashboard](#interactive-streamlit-dashboard)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Author and License](#author-and-license)

---

## Project Overview

As streaming services evolve into global media powerhouses, understanding catalog composition, licensing velocity, and target demographics provides critical strategic context. This project analyzes 8,807 titles across 12 metadata attributes to answer key business questions:

1. **Portfolio Composition**: What is the structural balance between feature films and serialized television?
2. **Geographic Footprint**: Which production ecosystems dominate the catalog, and how diversified is international sourcing?
3. **Temporal Dynamics**: When did catalog expansion accelerate, and what seasonal patterns govern title additions?
4. **Demographic Targeting**: How does maturity rating segmentation align with subscriber acquisition goals?
5. **Content Characteristics**: What are typical film durations, television run lengths, and acquisition lags from original release?
6. **Creative Talent Network**: Which directors and cast ensembles recur most frequently across original and licensed titles?

---

## Dataset Summary

The dataset originates from Kaggle's [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) collection, capturing catalog records up to September 2021.

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `show_id` | String | Unique identifier for each title |
| `type` | String | Content classification (`Movie` or `TV Show`) |
| `title` | String | Official release title |
| `director` | String | Director names (comma-separated for ensemble projects) |
| `cast` | String | Primary credited actors (comma-separated) |
| `country` | String | Production countries involved |
| `date_added` | Datetime | Date the content was onboarded to the platform |
| `release_year`| Integer | Original theatrical/television release year |
| `rating` | String | Age rating code (e.g., `TV-MA`, `TV-14`, `R`, `PG-13`) |
| `duration` | String | Runtime string (`min` for movies, `Season(s)` for series) |
| `listed_in` | String | Genre categories (comma-separated) |
| `description` | String | Narrative synopsis |

---

## Project Architecture

```text
Netflix Movies and Series/
│
├── Analysis/
│   └── Netflix_Data_Analysis.ipynb    # Complete 42-cell EDA research notebook
│
├── Dashboard/
│   ├── app.py                         # Streamlit multi-tab analytics application
│   └── requirements.txt               # Dashboard runtime dependencies
│
├── Dataset/
│   └── netflix_titles.csv             # Raw source dataset (8,807 rows)
│
└── README.md                          # Project documentation and findings report
```

---

## Data Preprocessing Pipeline

The analytical pipeline cleans and standardizes the dataset through five sequential stages:

1. **Rating Misalignment Correction**:
   - Identified and resolved records where duration strings (e.g., `74 min`, `84 min`) were displaced into the `rating` field.
   - Migrated duration values to their respective column and reset invalid rating fields.

2. **Categorical Imputation**:
   - Addressed missing entries in `director` (2,634 rows), `cast` (825 rows), and `country` (831 rows) by imputing standardized `'Unknown'` labels to prevent silent data truncation during aggregation.

3. **Critical Record Filtering**:
   - Dropped rows with missing `date_added`, `rating`, or `duration` values to maintain integrity in time-series and demographic evaluations (final cleaned volume: 8,790 titles).

4. **Temporal Feature Engineering**:
   - Converted `date_added` strings to standardized datetime objects.
   - Derived `year_added`, `month_added`, `month_name`, and `day_of_week`.
   - Engineered `lag_years` (`year_added - release_year`) to measure content age at acquisition.

5. **Metric Normalization**:
   - Extracted numeric duration (`duration_clean`) as minutes for movies and season counts for TV shows.

---

## Key Insights and Findings

### Executive Summary Metrics

| Metric | Value | Context |
| :--- | :--- | :--- |
| Total Analyzed Titles | 8,790 | Cleaned catalog records |
| Feature Films | 6,126 (69.7%) | Volume anchor of the library |
| Television Series | 2,664 (30.3%) | Primary driver of recurring engagement |
| Content Sourcing Nations | 123 | Unique production territories |
| Genre Categories | 42 | Granular content tags |
| Onboarding Period | 2008 - 2021 | Catalog intake window |
| Mean Movie Runtime | 100 minutes | Standard commercial feature duration |
| Mean Series Seasons | 1.8 seasons | Median at 1.0 season |
| Single-Season Shows | 67.4% | Reflects limited series and early cancellations |
| Leading Production Territory | United States | 3,680 titles (41.9%) |
| Leading Content Genre | International Movies | 2,752 titles |
| Modal Age Certification | TV-MA | 3,205 titles (36.5%) |

### Analytical Takeaways

1. **Core Catalog Sizing**: Feature films represent more than double the volume of television series. However, multi-season series create cumulative watch-time that exceeds per-title film consumption.
2. **International Sourcing Concentration**: While the United States remains the largest individual contributor, India (1,046 titles) and the United Kingdom (803 titles) represent critical regional production centers. Regional investments across South Korea, Japan, and Spain demonstrate focused expansion into non-English programming.
3. **Hyper-Growth Era (2016-2019)**: Title onboarding increased dramatically following Netflix's global launch across 130 countries in 2016, with annual additions peaking between 2018 and 2020 before stabilizing.
4. **Mature Audience Orientation**: `TV-MA` and `TV-14` together account for over 60% of all catalog entries, positioning Netflix primarily toward adult and young-adult demographics.
5. **Acquisition Lag Profile**: Approximately 26% of all titles enter the platform within the same calendar year as their original release, reflecting aggressive day-and-date licensing and original commissioning.

---

## Interactive Streamlit Dashboard

The repository includes a dark-themed, Netflix-branded interactive analytics dashboard located in `Dashboard/app.py`.

### Dashboard Capabilities

- **Overview Tab**: Metric KPI cards, interactive donut chart of content split, and stacked bar distribution of age certifications.
- **Geography Tab**: Top-N country production comparison with adjustable depth, multi-country split resolution, and US vs. International market share breakdown.
- **Time Series Tab**: Dual view by Year and Month, stacked area volume growth, year-over-year percentage change bars, and an interactive Year x Month onboarding heatmap.
- **Genre Tab**: Frequency analysis across all categories, type-specific genre rankings, and multi-line historical trend tracking for top genres over time.
- **Content Details Tab**: Movie duration histogram with mean/median reference lines, duration boxplots by age rating, television season distribution, and acquisition lag violin plots.
- **People Tab**: Prolific director rankings and most-credited actor rosters, filterable by content format.
- **Data Explorer Tab**: Searchable, sortable tabular data viewer with integrated CSV export capabilities.

---

## Tech Stack

- **Core Engine**: Python 3.8+
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visual Analytics**: [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Application Framework**: [Streamlit](https://streamlit.io/)
- **Notebook Environment**: [Jupyter Notebook](https://jupyter.org/) / VS Code

---

## Getting Started

### Prerequisites

Ensure Python 3.8 or higher is installed on your workstation.

### 1. Clone Repository

```bash
git clone https://github.com/NumiKun/Netflix-Movies-and-Series-Data-Analyze.git
cd "Netflix-Movies-and-Series-Data-Analyze"
```

### 2. Environment Setup

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install packages required for both the Jupyter Notebook and the Streamlit dashboard:

```bash
pip install -r Dashboard/requirements.txt matplotlib seaborn jupyter
```

### 4. Running the Jupyter Notebook

Open and execute the complete analytical pipeline:

```bash
jupyter notebook Analysis/Netflix_Data_Analysis.ipynb
```

### 5. Launching the Interactive Dashboard

Run the Streamlit application locally:

```bash
cd Dashboard
streamlit run app.py
```

The application will start at `http://localhost:8501`.

---

## Author and License

- **Author**: NumiKun
- **GitHub**: [@NumiKun](https://github.com/NumiKun)
- **Dataset**: [Kaggle - Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) by Shivam Bansal

Distributed under the MIT License. See `LICENSE` for details.
