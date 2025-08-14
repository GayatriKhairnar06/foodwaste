import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# -------------------
# Database Connection
# -------------------
DB_URL = "postgresql+psycopg2://postgres:Gayu123@localhost:5432/food_wastage"
engine = create_engine(DB_URL)

# -------------------
# Load Data Functions
# -------------------
@st.cache_data
def load_table(table_name):
    """Load a table from the database into a Pandas DataFrame."""
    return pd.read_sql_table(table_name, con=engine)

# -------------------
# Page Config
# -------------------
st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")
st.title("🍲 Local Food Wastage Management System")
st.markdown("Connecting surplus food providers to those in need")

# -------------------
# Load Data
# -------------------
providers_df = load_table("providers")
food_df = load_table("food_listings")

# -------------------
# Debug Info
# -------------------
st.write("### Preview: Providers Table")
st.dataframe(providers_df.head())
st.write("Columns in Providers Table:", providers_df.columns.tolist())

st.write("### Preview: Food Listings Table")
st.dataframe(food_df.head())
st.write("Columns in Food Listings Table:", food_df.columns.tolist())

# -------------------
# Sidebar Filters
# -------------------
st.sidebar.header("Filters")

# City filter
city_options = ["All"] + sorted(providers_df["city"].dropna().unique())
city_filter = st.sidebar.selectbox("Select City", city_options)

# Food type filter
food_type_options = ["All"] + sorted(food_df["food_type"].dropna().unique())
food_type_filter = st.sidebar.selectbox("Select Food Type", food_type_options)

# -------------------
# Display Providers
# -------------------
st.subheader("Providers")
filtered_providers = providers_df.copy()
if city_filter != "All":
    filtered_providers = filtered_providers[filtered_providers["city"] == city_filter]
st.dataframe(filtered_providers)

# -------------------
# Display Food Listings
# -------------------
st.subheader("Available Food Listings")
filtered_food = food_df.copy()
if food_type_filter != "All":
    filtered_food = filtered_food[filtered_food["food_type"] == food_type_filter]
st.dataframe(filtered_food)

# -------------------
# Chart: Total Food Listings by City
# -------------------
st.subheader("📊 Total Food Listings by City")
query = """
SELECT city, COUNT(*) AS total
FROM food_listings
GROUP BY city
"""
chart_df = pd.read_sql_query(query, con=engine)
fig = px.bar(chart_df, x="city", y="total", title="Food Listings by City")
st.plotly_chart(fig)

# -------------------
# CRUD Operations Example: Add Food
# -------------------
st.subheader("➕ Add New Food Listing")
with st.form("add_food_form"):
    name = st.text_input("Food Name")
    qty = st.number_input("Quantity", min_value=1)
    expiry = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1)
    provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
    city = st.text_input("City")
    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
    submitted = st.form_submit_button("Add Food")

    if submitted:
        insert_query = f"""
        INSERT INTO food_listings 
        (food_name, quantity, expiry_date, provider_id, provider_type, city, food_type, meal_type)
        VALUES ('{name}', {qty}, '{expiry}', {provider_id}, '{provider_type}', '{city}', '{food_type}', '{meal_type}')
        """
        with engine.begin() as conn:
            conn.execute(insert_query)
        st.success("✅ Food listing added successfully!")
