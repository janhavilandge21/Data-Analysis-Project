import streamlit as st
import pandas as pd

df = pd.read_csv(r"C:\Users\JANHAVI\Desktop\Data_Analyst_Project\sales_dataset_50k.csv")

st.title("AI Powered Sales Analytics Dashboard")

st.write("Dataset Overview")
st.dataframe(df.head())

st.subheader("Sales by Category")

category_sales = df.groupby('Category')['Sales'].sum()

st.bar_chart(category_sales)