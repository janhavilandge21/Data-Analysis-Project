# 📊 LLM-Powered Exploratory Data Analysis (EDA) App
This is an AI-powered EDA web application that allows users to upload a CSV dataset and automatically receive:

✅ A complete statistical summary

✅ Missing value report

✅ Data visualizations

✅ AI-generated insights using the Mistral-7B model via Ollama

✅ Clean and interactive user interface via Gradio

🔧 Features

Automatically fills missing numeric and categorical data.

Generates:

Histograms for each numeric feature

A correlation heatmap

Uses Ollama's Mistral-7B model to provide natural language analysis of the data summary.

Supports local file uploads (.csv) and produces downloadable EDA reports.

🖼 Sample Outputs

Distribution of Age	Correlation Heatmap	Distribution of Fare

Distribution of Parch	Pclass	Survived

🚀 How It Works

Upload a CSV file with tabular data.

The app cleans missing values:

Numeric → median

Categorical → mode

It generates summary statistics and visual plots.

The summary is passed to Ollama (Mistral-7B) for LLM-based insights.

The interface returns:

EDA summary text

Downloadable visualizations

🛠 Technologies Used

Python

Pandas – data handling

Matplotlib & Seaborn – visualization

Gradio – user interface

Ollama – chat-based LLM inference

Mistral-7B – model used for generating insights

⚙️ Setup Instructions

Install Ollama and Mistral model:


ollama run mistral

Install dependencies:


pip install gradio pandas matplotlib seaborn

Run the App:


python app1.py

Open the Gradio link (automatically generated) to use the web app.


🧠 Example Insight (from LLM)

"The dataset has a high concentration of passengers aged between 20–30. Fare distribution is right-skewed, indicating a few high-value outliers. Pclass and Fare are negatively correlated (-0.55), meaning higher-class passengers typically paid more..."
