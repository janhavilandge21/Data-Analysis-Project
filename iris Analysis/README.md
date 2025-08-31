# 🌸 IRIS Data Analysis & Visualization
📌 Project Overview

This project explores and visualizes the famous Iris Flower Dataset using Pandas, NumPy, Matplotlib, and Seaborn.
The goal is to analyze relationships between sepal & petal features across different species and demonstrate effective data visualization techniques.

📂 Dataset

Dataset: Iris.csv

Rows: 150

Columns:

SepalLengthCm

SepalWidthCm

PetalLengthCm

PetalWidthCm

Species (Setosa, Versicolor, Virginica)

🛠️ Technologies Used

Python 3

Pandas → Data handling & cleaning

NumPy → Numerical operations

Matplotlib → Plotting & charts

Seaborn → Statistical visualization

🔎 Key Analysis Steps

Data Preprocessing

Dropped unnecessary Id column

Checked missing values & data types

Exploratory Data Analysis (EDA)

Species distribution (count plot)

Descriptive statistics

Visualizations

Univariate Analysis: Histograms, Distplots

Bivariate Analysis: Jointplots, Pairplots, Scatterplots

Comparative Analysis: Boxplots, Stripplots, Violin plots

Advanced Visuals: Heatmaps, KDE plots, Catplots, Boxen plots, Stacked histograms, Area plots

📊 Insights & Findings

Setosa species has smaller petal lengths & widths compared to others.

Virginica flowers generally have the largest sepal & petal sizes.

Strong correlations exist between petal length & petal width.

Visualization confirms clear separation between species in feature space.

🚀 How to Run

Install dependencies:

pip install pandas numpy matplotlib seaborn


Run the Jupyter Notebook:

jupyter notebook "IRIS Analysis.ipynb"

📌 Future Improvements

Apply Machine Learning (KNN, SVM, Decision Trees) for species classification.

Build an interactive visualization dashboard (Streamlit/Plotly).

Compare results with scikit-learn’s Iris dataset utilities.
