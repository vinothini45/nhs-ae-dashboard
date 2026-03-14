import pandas as pd
import streamlit as st
import plotly.express as px

FILE = "https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2026/03/Monthly-AE-Time-Series-February-2026-D36ah6.xls"


df = pd.read_excel(FILE, sheet_name=0, header=13)
df = df[["Period", "Total Attendances",
         "Number of patients spending >4 hours from decision to admit to admission"]]
df.columns = ["date", "total_visits", "over_4_hours"]
df = df.dropna()
df["breach_rate"] = (df["over_4_hours"] / df["total_visits"] * 100).round(1)
df["date"] = pd.to_datetime(df["date"])

st.title("NHS A&E Waiting Time Analyser")
st.write("15 years of NHS England A&E data")

st.subheader("Breach rate over time")
fig = px.line(df, x="date", y="breach_rate",
              title="% patients waiting more than 4 hours",
              labels={"breach_rate": "Breach rate %", "date": "Month"})
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total months", len(df))
col2.metric("Avg breach rate", f"{df['breach_rate'].mean().round(1)}%")
col3.metric("Worst month", f"{df['breach_rate'].max().round(1)}%")