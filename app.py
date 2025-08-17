import streamlit as st
import psycopg2
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["neon"]["host"],
            dbname=st.secrets["neon"]["dbname"],
            user=st.secrets["neon"]["user"],
            password=st.secrets["neon"]["password"],
            port=st.secrets["neon"]["port"]
        )
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


# -----------------------------
# Fetch Data Function
# -----------------------------
def run_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return pd.DataFrame()


# -----------------------------
# App Layout
# -----------------------------
st.set_page_config(page_title="🍲 Food Waste Management", layout="wide")
st.title("🍲 Food Waste Management Dashboard")

st.markdown("### 📊 Explore food providers, receivers, and claims with filtering options.")

# -----------------------------
# Filters
# -----------------------------
city_filter = st.sidebar.text_input("🏙️ Filter by City")
provider_filter = st.sidebar.text_input("🏢 Filter by Provider Name")
food_type_filter = st.sidebar.text_input("🍛 Filter by Food Type")
meal_type_filter = st.sidebar.text_input("🥗 Filter by Meal Type")

# -----------------------------
# Example Queries (Replace with your 15 queries)
# -----------------------------
queries = {
    "All Providers": "SELECT * FROM \"Providers\"",
    "All Receivers": "SELECT * FROM \"Receivers\"",
    "All Food Listings": "SELECT * FROM \"Food_Listings\"",
    "All Claims": "SELECT * FROM \"Claims\"",
    "Providers with City Filter": """
        SELECT * FROM "Providers"
        WHERE (%s = '' OR "City" ILIKE %s)
    """,
    "Food Listings with Filters": """
        SELECT * FROM "Food_Listings"
        WHERE (%s = '' OR "Food_Type" ILIKE %s)
        AND (%s = '' OR "Meal_Type" ILIKE %s)
    """,
    "Providers & Contacts": """
        SELECT "Name", "Type", "City", "Contact"
        FROM "Providers"
        WHERE (%s = '' OR "Name" ILIKE %s)
    """,
    # You can add your other 12 queries here
}

# -----------------------------
# Display Query Results
# -----------------------------
st.subheader("📌 Query Results")

for name, query in queries.items():
    st.markdown(f"#### 🔹 {name}")
    if "City" in query:
        df = run_query(query, (city_filter, f"%{city_filter}%"))
    elif "Food_Type" in query:
        df = run_query(query, (food_type_filter, f"%{food_type_filter}%", meal_type_filter, f"%{meal_type_filter}%"))
    elif "Name" in query:
        df = run_query(query, (provider_filter, f"%{provider_filter}%"))
    else:
        df = run_query(query)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No records found for this query.")

