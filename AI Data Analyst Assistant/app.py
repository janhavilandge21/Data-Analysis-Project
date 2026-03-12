import streamlit as st
from ai_sql_agent import generate_sql, execute_query

st.title("AI Data Analyst Assistant")

question = st.text_input("Ask a question")

if question:

    sql = generate_sql(question)

    st.subheader("Generated SQL")
    st.code(sql)

    result = execute_query(sql)

    st.subheader("Result")
    st.write(result)