import pandas as pd
import re
import streamlit as st  # Needed for error display in Streamlit

class DataProcessor:
    def __init__(self, file):
        # Try to read the CSV with a forgiving encoding
        self.df = pd.read_csv(file, encoding='utf-8-sig')

        # Print columns for debugging
        print("Columns found in CSV:", self.df.columns.tolist())

    def clean_data(self):
        df = self.df.copy()
        # Check for 'Text' column
        if 'Text' not in df.columns:
            st.error("❌ Error: Required 'Text' column not found in CSV. Columns found: {}".format(df.columns.tolist()))
            st.stop()  # Stop the Streamlit app
        df.dropna(subset=['Text'], inplace=True)
        return df

    def combine_datetime(self, df):
        df = df.copy()
        # Convert year, month, day, hour to integers to remove .0
        for col in ['Year', 'Month', 'Day', 'Hour']:
            if col not in df.columns:
                st.error(f"❌ Error: Required '{col}' column not found in CSV. Columns found: {df.columns.tolist()}")
                st.stop()
            df[col] = df[col].astype(int)
        # Build the datetime string
        df['datetime_str'] = (
            df['Year'].astype(str) + '-' +
            df['Month'].astype(str).str.zfill(2) + '-' +
            df['Day'].astype(str).str.zfill(2) + ' ' +
            df['Hour'].astype(str).str.zfill(2) + ':00:00'
        )
        df['datetime'] = pd.to_datetime(df['datetime_str'], format="%Y-%m-%d %H:%M:%S")
        return df

    def extract_hashtags(self, df):
        df = df.copy()
        # Check for 'Hashtags' column
        if 'Hashtags' not in df.columns:
            st.error("❌ Error: Required 'Hashtags' column not found in CSV. Columns found: {}".format(df.columns.tolist()))
            st.stop()
        # Extract hashtags from the Hashtags column
        df['hashtags'] = df['Hashtags'].fillna('').apply(lambda x: re.findall(r'#\w+', str(x)))
        return df

    def get_trend_data(self, df, interval='D'):
        df = self.combine_datetime(df)
        df = self.extract_hashtags(df)
        exploded = df.explode('hashtags')
        exploded = exploded[exploded['hashtags'].notna() & (exploded['hashtags'] != '')]
        grouped = exploded.groupby([
            pd.Grouper(key='datetime', freq=interval),
            'hashtags'
        ]).size().reset_index(name='count')
        return grouped
