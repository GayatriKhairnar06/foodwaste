import streamlit as st
import psycopg2
import pandas as pd

# ==============================
# Database Connection Function
# ==============================
def get_db_connection():
    return psycopg2.connect(
        host=st.secrets["neon"]["host"],
        dbname=st.secrets["neon"]["dbname"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=st.secrets["neon"]["port"],
        sslmode="require"   # 🔑 Important for Neon Cloud DB
    )

# ==============================
# Load Data Function
# ==============================
@st.cache_data
def load_data():
    conn = get_db_connection()
    query = """
        SELECT 
            f."Food_ID",
            f."Food_Type",
            f."Meal_Type",
            f."Quantity",
            p."Name" AS provider_name,
            p."Type" AS provider_type,
            p."City",
            p."Contact"
        FROM "Food_Listings" f
        JOIN "Providers" p ON f."Provider_ID" = p."Provider_ID";
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ==============================
# Streamlit App
# ==============================
st.set_page_config(page_title="Food Waste Management", layout="wide")
st.title("🍲 Food Waste Management Dashboard")

# Load data
df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

city_filter = st.sidebar.selectbox("City", ["All"] + sorted(df["City"].dropna().unique().tolist()))
provider_type_filter = st.sidebar.selectbox("Provider Type", ["All"] + sorted(df["provider_type"].dropna().unique().tolist()))
food_type_filter = st.sidebar.selectbox("Food Type", ["All"] + sorted(df["Food_Type"].dropna().unique().tolist()))
meal_type_filter = st.sidebar.selectbox("Meal Type", ["All"] + sorted(df["Meal_Type"].dropna().unique().tolist()))

# Apply filters
filtered_df = df.copy()

if city_filter != "All":
    filtered_df = filtered_df[filtered_df["City"] == city_filter]

if provider_type_filter != "All":
    filtered_df = filtered_df[filtered_df["provider_type"] == provider_type_filter]

if food_type_filter != "All":
    filtered_df = filtered_df[filtered_df["Food_Type"] == food_type_filter]

if meal_type_filter != "All":
    filtered_df = filtered_df[filtered_df["Meal_Type"] == meal_type_filter]

# Show Results
st.subheader("📋 Available Food Listings")

if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters.")
else:
    st.dataframe(filtered_df, use_container_width=True)

    # Provider Contact Info
    st.subheader("📞 Provider Contact Details")
    contact_df = filtered_df[["provider_name", "provider_type", "City", "Contact"]].drop_duplicates()
    st.table(contact_df)
