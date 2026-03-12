from langchain_groq import ChatGroq
import sqlite3
import pandas as pd
import re

# Initialize LLM
llm = ChatGroq(
    groq_api_key="",
    model_name="llama-3.1-8b-instant"
)

# Clean SQL returned by LLM
def clean_sql(text):

    text = text.replace("```sql", "").replace("```", "")

    match = re.search(r"(SELECT .*?;)", text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1)

    return text.strip()


# Generate SQL from user question
def generate_sql(question):

    prompt = f"""
Return ONLY a valid SQLite SQL query.

Table: sales

Columns:
Order_ID
Region
Category
Sales
Profit
Quantity

Question: {question}

Only return SQL query.
"""

    response = llm.invoke(prompt)

    sql = clean_sql(response.content)

    return sql


# Execute SQL query
def execute_query(sql):

    conn = sqlite3.connect("sales_database.db")

    result = pd.read_sql(sql, conn)

    conn.close()

    return result