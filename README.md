# 🎬 Netflix Movies & TV Shows Data Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blueviolet.svg)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end **Exploratory Data Analysis (EDA)** and Data Preprocessing project exploring Netflix's global catalog of movies and TV shows up to 2021. This project uncovers content distribution patterns, global production hubs, release timelines, target demographics, and strategic shifts in Netflix's streaming catalog.

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Dataset Summary](#-dataset-summary)
- [Project Structure](#-project-structure)
- [Data Cleaning & Preparation](#-data-cleaning--preparation)
- [Key Insights & Findings](#-key-insights--findings)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Future Enhancements](#-future-enhancements)
- [Author & Acknowledgments](#-author--acknowledgments)

---

## 📖 Project Overview

Netflix is one of the world's leading entertainment streaming services. Understanding its catalog composition reveals important strategic insights about:
- Content prioritization (Movies vs. TV Series)
- Global market expansion & regional investments (e.g., US, India, UK, East Asia)
- Target audience segmentation through content ratings (e.g., TV-MA, TV-14)
- Growth dynamics and catalog updates over time

This portfolio project delivers a clean, reproducible analytical pipeline built with **Python**, **Pandas**, and **Seaborn/Matplotlib** in a Jupyter Notebook.

---

## 📊 Dataset Summary

The dataset consists of **8,807 rows** and **12 columns**, capturing comprehensive metadata for Netflix titles up to late 2021.

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `show_id` | String | Unique identifier for each title (e.g., `s1`, `s2`) |
| `type` | String | Content category (`Movie` or `TV Show`) |
| `title` | String | Title of the movie or series |
| `director` | String | Director(s) of the content |
| `cast` | String | Main actors / cast members |
| `country` | String | Country/countries involved in production |
| `date_added` | String / Date | Date the title was added to Netflix |
| `release_year`| Integer | Original release year (1925 – 2021) |
| `rating` | String | Age rating / content certification (e.g., `TV-MA`, `PG-13`) |
| `duration` | String | Duration in minutes (`min`) or number of seasons (`Season(s)`) |
| `listed_in` | String | Genres / categories (comma-separated) |
| `description` | String | Brief synopsis / plot summary |

---

## 📁 Project Structure

```text
Netflix Movies and Series/
│
├── Analysis/
│   └── Netflix_Data_Analysis.ipynb    # Main Jupyter Notebook with complete EDA pipeline
│
├── Dataset/
│   └── netflix_titles.csv             # Raw Netflix dataset
│
└── README.md                          # Project documentation & insights report
```

---

## 🛠️ Data Cleaning & Preparation

Before conducting exploratory analysis, the dataset underwent systematic preprocessing:

1. **Handling Data Misalignments**:
   - Fixed entries where movie duration values (e.g., `74 min`, `84 min`, `66 min`) were misplaced in the `rating` column.
2. **Missing Value Imputation**:
   - Replaced missing values in categorical fields (`director`, `cast`, `country`) with `'Unknown'`.
   - Handled rare missing records in `date_added`, `rating`, and `duration`.
3. **Feature Engineering & Type Casting**:
   - Parsed `date_added` into standardized `datetime` objects.
   - Extracted `year_added` and `month_added` to evaluate temporal trends.

---

## 💡 Key Insights & Findings

### 1. Movie Dominance vs. TV Shows
* **Movies** comprise **~69.6% (6,131 titles)** of the catalog, while **TV Shows** make up **~30.4% (2,676 titles)**.
* Movies remain the core volume driver, although multi-season TV shows provide higher recurring viewer engagement.

### 2. Top Content Producing Nations
* **United States** leads global production by a large margin (**2,800+ titles**).
* **India** is the second-largest content contributor (**970+ titles**), highlighting Netflix's massive investment in Bollywood and Indian regional cinema.
* Other major hubs include the **United Kingdom**, **Japan**, **South Korea**, **Canada**, and **Spain**.

### 3. Rapid Catalog Expansion (2016–2020)
* Content additions on Netflix surged exponentially starting in **2016**, reaching peak intake between **2018 and 2020**.
* This aligns with Netflix's aggressive global expansion and pivot toward Netflix Originals.

### 4. Audience Demographics & Ratings
* **TV-MA** (Mature Audiences / Adults) is the single largest category (**>36%** of all content), followed by **TV-14** (**>24%**).
* Netflix’s catalog strongly targets young adults and mature demographics, while maintaining family/kids programming (`TV-PG`, `TV-Y7`, `PG`).

---

## 💻 Tech Stack

- **Language**: Python 3.8+
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Data Visualization**: [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Environment**: [Jupyter Notebook](https://jupyter.org/) / VS Code

---

## 🚀 Getting Started

Follow these steps to run the analysis locally:

### 1. Clone the Repository
```bash
git clone https://github.com/NumiKun/Netflix-Movies-and-Series-Data-Analyze.git
cd Netflix-Movies-and-Series-Data-Analyze
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook Analysis/Netflix_Data_Analysis.ipynb
```

---

## 🔮 Future Enhancements

- [ ] **Content-Based Recommendation Engine**: Implement TF-IDF and Cosine Similarity on `description`, `cast`, and `listed_in`.
- [ ] **NLP & Sentiment Analysis**: Analyze synopsis text to identify recurring themes and genre sentiment trends.
- [ ] **Interactive Web Dashboard**: Build an interactive dashboard using **Streamlit** or **Dash** with dynamic multi-filter capabilities.

---

## 👤 Author & Acknowledgments

- **Author**: NumiKun
- **GitHub**: [@NumiKun](https://github.com/NumiKun)
- **Dataset Source**: Netflix Movies and TV Shows Dataset ([Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows))

---
*Distributed under the MIT License. See `LICENSE` for more information.*
