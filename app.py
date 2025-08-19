import streamlit as st
import psycopg2
import pandas as pd

# -------------------------
# Database connection
# -------------------------
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
        st.error(f"Database connection failed: {e}")
        return None

# -------------------------
# Query function
# -------------------------
def run_query(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# -------------------------
# Streamlit App
# -------------------------
st.title("🍴 Food Waste Management Dashboard")

st.write("Filter food availability & requests from the database")

# Dropdown filters
city_filter = st.selectbox(
    "Select City",
    ["All"] + run_query('SELECT DISTINCT "City" FROM "Providers"')["City"].dropna().tolist()
)

provider_filter = st.selectbox(
    "Select Provider",
    ["All"] + run_query('SELECT DISTINCT "Name" FROM "Providers"')["Name"].dropna().tolist()
)

food_type_filter = st.selectbox(
    "Select Food Type",
    ["All"] + run_query('SELECT DISTINCT "Food_Type" FROM "Food_Listings"')["Food_Type"].dropna().tolist()
)

meal_type_filter = st.selectbox(
    "Select Meal Type",
    ["All"] + run_query('SELECT DISTINCT "Meal_Type" FROM "Food_Listings"')["Meal_Type"].dropna().tolist()
)

# Build dynamic query
query = """
SELECT f."Food_ID", f."Food_Name", f."Food_Type" AS "Food Type",
       f."Meal_Type" AS "Meal Type", f."Quantity", f."Expiry_Date",
       p."Name" AS "Provider", p."Type" AS "Provider Type",
       p."City", p."Contact"
FROM "Food_Listings" f
JOIN "Providers" p ON f."Provider_ID" = p."Provider_ID"
WHERE 1=1
"""

filters = []
params = []

if city_filter != "All":
    filters.append('p."City" = %s')
    params.append(city_filter)
if provider_filter != "All":
    filters.append('p."Name" = %s')
    params.append(provider_filter)
if food_type_filter != "All":
    filters.append('f."Food_Type" = %s')
    params.append(food_type_filter)
if meal_type_filter != "All":
    filters.append('f."Meal_Type" = %s')
    params.append(meal_type_filter)

if filters:
    query += " AND " + " AND ".join(filters)

# Fetch data
df = run_query(query, params)

if df.empty:
    st.warning("⚠️ No records found for the selected filters.")
else:
    st.dataframe(df)

    # Show provider contact details
    with st.expander("📞 Show Provider Contact Details"):
        st.table(df[["Provider", "Contact"]].drop_duplicates())
