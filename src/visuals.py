import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("🧠 Natural Language to Data Visualization")

# User input
query = st.text_input("Enter your query (e.g., 'Show sales by region for Q1')")

# Simulated query understanding and data fetch
def get_simulated_data(query):
    if "sales" in query.lower() and "region" in query.lower():
        df = pd.DataFrame({
            'Region': ['North', 'South', 'East', 'West'],
            'Sales': np.random.randint(1000, 5000, 4)
        })
        return df, "bar", "Sales by Region"
    
    elif "monthly" in query.lower() or "trend" in query.lower():
        df = pd.DataFrame({
            'Month': pd.date_range(start='2024-01-01', periods=6, freq='M').strftime('%b'),
            'Revenue': np.random.randint(10000, 30000, 6)
        })
        return df, "line", "Monthly Revenue Trend"
    
    else:
        df = pd.DataFrame({
            'Category': ['A', 'B', 'C'],
            'Value': np.random.randint(10, 100, 3)
        })
        return df, "pie", "Example Pie Chart"

# Handle query and visualize
if query:
    df, chart_type, title = get_simulated_data(query)
    st.subheader(title)
    st.dataframe(df)

    if chart_type == "bar":
        st.bar_chart(df.set_index('Region'))
    elif chart_type == "line":
        st.line_chart(df.set_index('Month'))
    elif chart_type == "pie":
        fig, ax = plt.subplots()
        ax.pie(df['Value'], labels=df['Category'], autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
