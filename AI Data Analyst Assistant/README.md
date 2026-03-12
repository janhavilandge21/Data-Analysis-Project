# 🤖 AI Data Analyst Assistant


An **AI-powered Data Analytics system** that allows users to analyze business data using **natural language queries**.

Instead of writing complex SQL queries manually, users can simply type questions like:

* *“Total sales by region”*
* *“Top 5 products by sales”*
* *“Average profit by category”*

The system automatically:

1. Converts the question into SQL using a Large Language Model
2. Executes the query on a database
3. Displays results in an interactive analytics dashboard

This project demonstrates how **Generative AI can simplify data analysis for non-technical business users**.

---

# 📊 Dashboard Preview

## 1️⃣ Business Analytics Dashboard

![Business Analytics Dashboard](images/dashboard1.png)

This dashboard shows important **business KPIs and performance metrics**, including:

### Key Metrics

* Total Pageviews
* Unique Users
* Total Sessions
* Average Session Duration
* Bounce Rate

### Data Visualizations

* Daily Unique Visitors Trend
* Pageviews by Date
* Session Duration Analysis
* User Engagement Metrics

These visualizations help organizations understand **user behavior and website performance trends**.

---

## 2️⃣ SQL Query and Data Exploration Interface

![SQL Query Dashboard](images/dashboard2.png)

This interface allows analysts to:

* Write and execute **SQL queries**
* Retrieve data from connected databases
* Explore datasets interactively
* View results in structured tables
* Perform **data exploration and analysis**

The system also supports **AI-generated queries based on natural language input**.

---

# 🧠 System Architecture

The system follows a simple **AI-powered analytics pipeline**.

User Question
↓
LLM converts question → SQL query
↓
SQL query executes on database
↓
Data retrieved from database
↓
Results visualized in dashboard

---

# ⚙️ Project Workflow

### Step 1 — User Input

The user enters a question in natural language.

Example:

```id="5vsvd2"
Total sales by region
```

---

### Step 2 — AI Query Generation

The Large Language Model converts the question into SQL.

Example SQL generated:

```sql id="4k0f3u"
SELECT Region, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region;
```

---

### Step 3 — Query Execution

The SQL query is executed on the database using Python and SQLite.

---

### Step 4 — Result Visualization

The system displays:

* Data tables
* Charts
* Analytics insights

---

# 🛠 Technology Stack

### Programming Language

* Python

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### AI / NLP

* LangChain
* Groq LLM

### Database

* SQLite
* MySQL (optional)

### Dashboard Framework

* Streamlit

---

# 📁 Project Structure

```id="6krsjz"
AI-Data-Analyst-Agent

data/
   sales_dataset.csv

images/
   dashboard1.png
   dashboard2.png

app.py
ai_sql_agent.py
database_setup.py
sales.db

README.md
requirements.txt
```

---

# ⚙️ Installation Guide

Clone the repository

```id="nd2o1o"
git clone https://github.com/yourusername/ai-data-analyst-agent.git
```

Move into project directory

```id="yhdm5j"
cd ai-data-analyst-agent
```

Install dependencies

```id="n6k0d6"
pip install pandas streamlit langchain langchain-groq matplotlib
```

---

# ▶️ Running the Application

Start the Streamlit dashboard

```id="qclq4s"
streamlit run app.py
```

Open browser

```id="xv3j6k"
http://localhost:8501
```

---

# 💬 Example Questions to Try

You can ask the system questions such as:

```id="7g9r6o"
Total sales by region
```

```id="utndpw"
Top 5 products by sales
```

```id="hdbd3c"
Average profit by category
```

```id="4c2v5z"
Which region has highest sales
```

The AI will automatically generate SQL queries and return results.

---

# 📊 Business Insights Example

Using the analytics dashboard we can discover insights like:

* The **West region generates the highest revenue**
* **Electronics category contributes most sales**
* Customer engagement peaks during specific time periods
* Bounce rate indicates user experience issues on certain pages

These insights help businesses **make data-driven decisions**.

---

# 🚀 Future Improvements

Possible improvements for the project include:

* Automated chart generation
* AI explanation of insights
* Integration with cloud databases
* Real-time data streaming
* Multi-dataset analysis
* Deployment using Docker or cloud platforms

---
