# 🤖 AI Data Analyst Assistant

An AI-powered analytics tool that allows users to analyze business data using **natural language queries**.

The system converts user questions into **SQL queries using an LLM**, executes them on a database, and displays results through an **interactive Streamlit dashboard**.

---

# 📊 Dashboard

![Dashboard](images/dashboard.png)

The dashboard allows users to ask questions like:

* Total sales by region
* Top 5 products by sales
* Average profit by category

The AI automatically generates SQL queries and returns results.

---

# 🧠 System Architecture

![Architecture](images/architecture.png)

Workflow:

1. User enters a question
2. LLM converts question → SQL query
3. SQL query runs on database
4. Results displayed on dashboard

---

# 🛠 Tech Stack

**Programming**

* Python

**Libraries**

* Pandas
* Matplotlib
* LangChain
* Groq LLM

**Database**

* SQLite

**Dashboard**

* Streamlit

---

# 📁 Project Structure

```
AI-Data-Analyst-Agent

data/
   sales_dataset.csv

ai_sql_agent.py
app.py
database_setup.py
sales.db

images/
   dashboard.png
   architecture.png

README.md
```

---

# ⚙️ Installation

Clone the repository

```
git clone https://github.com/yourusername/ai-data-analyst-agent.git
```

Move into project folder

```
cd ai-data-analyst-agent
```

Install dependencies

```
pip install pandas streamlit langchain langchain-groq matplotlib
```

---

# ▶️ Run Application

```
streamlit run app.py
```

Open browser

```
http://localhost:8501
```

---

# 💬 Example Questions

Try asking:

```
Total sales by region
```

```
Top 5 products by sales
```

```
Average profit by category
```

---

# 📊 Key Features

* Natural language to SQL conversion
* Automated business analytics
* Interactive dashboard
* AI-powered insights

---

