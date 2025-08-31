# 📊 Country GDP Economy Analysis
📌 Project Overview

This project analyzes the relationship between GDP indicators, birth rate, internet usage, and income groups across different countries.
It uses data analysis, visualization, and filtering techniques to identify patterns in economic growth and digital adoption.

📂 Dataset

The dataset (data.csv) contains 195 countries with the following columns:

CountryName → Name of the country

CountryCode → ISO country code

BirthRate → Number of births per 1,000 people

InternetUsers → Percentage of internet users

IncomeGroup → World Bank income classification (High, Upper Middle, Lower Middle, Low)

🛠️ Technologies Used

Python 3

Pandas → Data cleaning & manipulation

NumPy → Numerical computations

Matplotlib & Seaborn → Data visualization

🔎 Key Analysis Steps

Data Exploration

Loaded CSV into Pandas DataFrame.

Checked shape, null values, and descriptive statistics.

Filtering & Selection

Extracted subsets (e.g., High income countries, BirthRate > 40).

Added new computed columns.

Visualization

Distribution of Internet Users.

Boxplot: IncomeGroup vs BirthRate.

Scatter plot with regression: InternetUsers vs BirthRate.

📊 Insights & Findings

High birth rates are generally found in low-income countries.

Internet penetration is strongly correlated with higher income levels.

Countries with higher internet usage tend to have lower birth rates.

🚀 How to Run

Run the Jupyter Notebook:

jupyter notebook "Country GDP Economy Analysis.ipynb"

📈 Visualizations

📌 Distribution Plot → Internet users across countries

📌 Boxplot → Birth rate by income group

📌 Regression Plot → Internet users vs. birth rate

📌 Future Improvements

Add GDP per capita for deeper insights.

Build interactive dashboards using Power BI / Plotly.

Perform time-series analysis with historical data.
