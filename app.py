import streamlit as st
import pandas as pd

# Load your CSV
providers_df = pd.read_csv("providers_data.csv")

# Normalize column names: strip spaces and convert to lowercase
providers_df.columns = providers_df.columns.str.strip().str.lower()

# Check if 'city' column exists
if 'city' in providers_df.columns:
    city_options = ["All"] + sorted(providers_df["city"].dropna().unique())
else:
    st.warning("Column 'city' not found in providers data.")
    city_options = ["All"]  # Fallback

# Example Streamlit selectbox
selected_city = st.selectbox("Select City", city_options)

# Rest of your code
st.write("Selected city:", selected_city)
