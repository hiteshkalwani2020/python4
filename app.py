import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor
from utils.visualizations import plot_trends

st.title("Content Trend Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file (PAPA.csv format)", type="csv")

if uploaded_file:
    processor = DataProcessor(uploaded_file)
    df = processor.clean_data()
else:
    st.info("Or use the sample data below (PAPA.csv).")
    processor = DataProcessor("data/PAPA.csv")
    df = processor.clean_data()

st.write("Sample Data", df.head())

interval = st.selectbox(
    "Time Interval",
    options=[('Hour', 'H'), ('Day', 'D'), ('Week', 'W')],
    format_func=lambda x: x[0]
)
top_n = st.slider("Number of top hashtags to show", min_value=1, max_value=10, value=5)

trend_df = processor.get_trend_data(df, interval=interval[1])
if not trend_df.empty:
    fig = plot_trends(trend_df, top_n=top_n)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hashtags found in the data.")
