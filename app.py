import streamlit as st
import psycopg2
import pandas as pd


# ========================
# Database Connection
# ========================
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["neon"]["host"],  # your Neon host
            database=st.secrets["neon"]["dbname"],  # your database name
            user=st.secrets["neon"]["user"],  # your db user
            password=st.secrets["neon"]["password"],  # your password
            port=st.secrets["neon"]["port"]  # db port (5432)
        )
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


# ========================
# Fetch Query
# ========================
def run_query(query):
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ Query failed: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


# ========================
# Streamlit UI
# ========================
st.set_page_config(page_title="Food Waste Management", layout="wide")
st.title("🥗 Food Waste Management System")

# Sidebar
menu = st.sidebar.radio("Navigation", ["Providers", "Receivers", "Food Listings", "Claims", "Search"])

# ========================
# Providers
# ========================
if menu == "Providers":
    st.subheader("👨‍🌾 Providers List")
    df = run_query('SELECT * FROM "providers_data";')
    st.dataframe(df)

# ========================
# Receivers
# ========================
elif menu == "Receivers":
    st.subheader("🤝 Receivers List")
    df = run_query('SELECT * FROM "receivers_data";')
    st.dataframe(df)

# ========================
# Food Listings
# ========================
elif menu == "Food Listings":
    st.subheader("🍲 Available Food Listings")
    df = run_query('SELECT * FROM "food_listings_data";')
    st.dataframe(df)

# ========================
# Claims
# ========================
elif menu == "Claims":
    st.subheader("📦 Food Claims")
    df = run_query('SELECT * FROM "Claims_data";')
    st.dataframe(df)

# ========================
# Search & Filter
# ========================
elif menu == "Search":
    st.subheader("🔎 Search & Filter Food")
    city = st.text_input("Enter City")
    food_type = st.text_input("Enter Food Type")

    query = 'SELECT * FROM "Food_Listings" fl JOIN "Providers" p ON fl."Provider_ID" = p."Provider_ID" WHERE 1=1'
    if city:
        query += f" AND p.\"City\" ILIKE '%{city}%'"
    if food_type:
        query += f" AND fl.\"Type\" ILIKE '%{food_type}%'"

    df = run_query(query)
    st.dataframe(df)
