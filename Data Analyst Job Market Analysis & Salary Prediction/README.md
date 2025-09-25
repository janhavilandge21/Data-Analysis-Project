# Data Analyst Job Market Analysis & Salary Prediction

**Project summary**

This repository contains a data analysis and salary-prediction project based on scraped Data Analyst job listings (Glassdoor-style). The project performs cleaning, exploratory data analysis (EDA), feature engineering, visualization, and a simple machine learning model to predict annual salaries. A minimal Streamlit app is included to demo the salary prediction.

## Contents

* `DataAnalyst.csv` — raw dataset (2253 rows).
* `notebooks/` — Jupyter notebooks containing EDA, cleaning, feature engineering, model building, and visualizations.
* `scripts/` — helper scripts for parsing and preprocessing (salary parsing, location parsing, etc.).
* `streamlit_app.py` — lightweight Streamlit front-end to demo the trained model.
* `README.md` — this file.

## Dataset overview

* **Rows**: 2253
* **Features (high level)**: Job Title, Salary Estimate, Job Description, Rating, Company Name, Location, Headquarters, Size, Founded, Type of ownership, Industry, Sector, Revenue, Competitors, Easy Apply
* Many derived fields are created during processing: `Min_Annual`, `Max_Annual`, `Avg_Annual`, `Is_Hourly`, `Min_K`, `Avg_K`, `City`, `State`, `Python`, `Excel`, `Tech_Skills`, etc.

## Key preprocessing steps

1. **Column cleaning & renaming** — standardized column names and removed unnecessary columns (e.g. `Unnamed: 0`).
2. **Salary parsing** — robust parser that handles ranges, `K` suffixes, hourly vs. yearly wages, employer-provided notes and Glassdoor estimation text. Hourly values are converted to annual using 2080 hours/year.
3. **Missing values** — `Rating` filled with median; columns with >30% missing were dropped; categorical forward-fill for a few fields.
4. **Location parsing** — split `Location` into `City` and `State`, handled remote keywords (`remote`, `work from home`, `wfh`, `anywhere`).
5. **Feature engineering** — extracted presence of skills (`Python`, `Excel`) from job descriptions; created `Tech_Skills` (count) and salary-aggregates in K (`Min_K`, `Avg_K`, `Max_K`).

## Exploratory Data Analysis (EDA)

* Distribution of salary estimates (histograms / KDE).
* Top job titles and counts (Data Analyst, Senior Data Analyst, Junior Data Analyst, etc.).
* Salary by job title and company size visualizations (bar plots, boxen/boxplots).
* Company ratings by industry (boxplots).
* Correlation heatmap for numeric features.

## Modeling

* **Model**: RandomForestRegressor (scikit-learn)
* **Features used (example)**: `Rating`, `Tech_Skills`, `Size` (label-encoded), `Founded`
* **Target**: `Avg_Annual` (and in alternatives `Avg_K`)
* **Train/test split**: 80/20, `random_state=42`

**Reported performance (baseline)**

* MAE: ~21,180 (USD)
* R²: negative (model underperforms baseline on held-out data)

> Notes: performance indicates either insufficient/predictive features for salary or need for richer feature engineering, more data, or different modeling approaches. See "Next steps" below.

## Visualizations

The notebooks include code for generating Matplotlib/Seaborn and Plotly visualizations such as:

* Salary distribution and boxplots
* Top job titles and locations
* Average salary by job title and company size
* Heatmap of numeric correlations

## Requirements

Create a `requirements.txt` with (example):

```
pandas
numpy
scikit-learn
matplotlib
seaborn
plotly
streamlit
```

(Use `pip freeze > requirements.txt` from your environment to produce an exact list.)

## Reproducibility

* Notebooks contain the full data-loading and preprocessing pipeline. To reproduce results, start by running the cleaning/feature-engineering notebook then the modeling notebook.
* Make sure to set the same random seed used during `train_test_split` and model initialization for reproducible training.

## Observations & Takeaways

* Salary parsing is tricky: strings contain `Glassdoor est.`, `employer provided` notes, hourly rates, and `K` suffixes — the included parser aims to normalize these into numeric annual salaries.
* The baseline Random Forest had poor predictive performance (high MAE and negative R²), suggesting:

  * Need for additional predictive features (e.g., exact role seniority extracted from titles, company revenue/industry embedding, location cost-of-living adjustment).
  * Try other models (XGBoost / LightGBM), hyperparameter tuning, and cross-validation.
  * Consider log-transforming salary targets or modelling classification buckets instead of raw regression.

## Next steps / Improvements

* Improve text feature extraction from job descriptions (NLP features: TF-IDF, embeddings, named-entity extraction for skills and seniority).
* Use external data to enrich company features (e.g., company revenue, market cap, or cost-of-living indices per city).
* Hyperparameter tuning and model ensembling.
* Handle outliers, and consider log-scaling the target variable.
* Add unit tests for parsing functions (salary and location parsers).
