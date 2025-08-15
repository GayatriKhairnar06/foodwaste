import streamlit as st
import psycopg2
import pandas as pd

# -------------------------------
# Database Connection
# -------------------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="food_waste_db",
        user="postgres",
        password="yourpassword"
    )

# -------------------------------
# Execute Query Function
# -------------------------------
def run_query(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.set_page_config(page_title="Food Wastage Insights", layout="wide")
st.title("🍽 Food Wastage Management Dashboard")

# Sidebar for Query Selection
queries = {
    "1️⃣ Top 5 Food Providers": """
        SELECT provider_name, COUNT(*) AS total_donations
        FROM food_donations
        GROUP BY provider_name
        ORDER BY total_donations DESC
        LIMIT 5;
    """,
    "2️⃣ Most Donated Food Types": """
        SELECT food_type, COUNT(*) AS frequency
        FROM food_donations
        GROUP BY food_type
        ORDER BY frequency DESC
        LIMIT 5;
    """,
    "3️⃣ Locations with Highest Claims": """
        SELECT location, COUNT(*) AS claim_count
        FROM food_claims
        GROUP BY location
        ORDER BY claim_count DESC
        LIMIT 5;
    """,
    "4️⃣ Average Quantity per Donation": """
        SELECT AVG(quantity) AS avg_quantity
        FROM food_donations;
    """,
    "5️⃣ Providers with Maximum Quantity Donated": """
        SELECT provider_name, SUM(quantity) AS total_quantity
        FROM food_donations
        GROUP BY provider_name
        ORDER BY total_quantity DESC
        LIMIT 5;
    """,
    "6️⃣ Food Type Trends (Donations over Time)": """
        SELECT food_type, DATE(donation_date) AS date, COUNT(*) AS donations
        FROM food_donations
        GROUP BY food_type, DATE(donation_date)
        ORDER BY date ASC;
    """,
    "7️⃣ Top Receivers of Food": """
        SELECT receiver_name, COUNT(*) AS total_claims
        FROM food_claims
        GROUP BY receiver_name
        ORDER BY total_claims DESC
        LIMIT 5;
    """,
    "8️⃣ Wastage by Food Type": """
        SELECT food_type, SUM(quantity) AS wasted_quantity
        FROM food_wastage
        GROUP BY food_type
        ORDER BY wasted_quantity DESC
        LIMIT 5;
    """,
    "9️⃣ Providers with Most Wastage": """
        SELECT provider_name, SUM(quantity) AS wasted_quantity
        FROM food_wastage
        GROUP BY provider_name
        ORDER BY wasted_quantity DESC
        LIMIT 5;
    """,
    "🔟 Total Donations vs Claims": """
        SELECT (SELECT COUNT(*) FROM food_donations) AS total_donations,
               (SELECT COUNT(*) FROM food_claims) AS total_claims;
    """,
    "11️⃣ Monthly Donation Trends": """
        SELECT DATE_TRUNC('month', donation_date) AS month, COUNT(*) AS donations
        FROM food_donations
        GROUP BY month
        ORDER BY month ASC;
    """,
    "12️⃣ Location-wise Donation Count": """
        SELECT location, COUNT(*) AS donations
        FROM food_donations
        GROUP BY location
        ORDER BY donations DESC;
    """,
    "13️⃣ Most Frequent Provider per Location": """
        SELECT location, provider_name, COUNT(*) AS donation_count
        FROM food_donations
        GROUP BY location, provider_name
        ORDER BY location, donation_count DESC;
    """,
    "14️⃣ Average Time to Claim Donation": """
        SELECT AVG(claim_time - donation_time) AS avg_claim_duration
        FROM food_claims;
    """,
    "15️⃣ Providers with Zero Wastage": """
        SELECT fd.provider_name
        FROM food_donations fd
        LEFT JOIN food_wastage fw ON fd.provider_name = fw.provider_name
        WHERE fw.provider_name IS NULL
        GROUP BY fd.provider_name;
    """
}

# -------------------------------
# UI: Select and Execute Queries
# -------------------------------
selected_query = st.sidebar.selectbox("📊 Choose an Analysis Query", list(queries.keys()))
st.subheader(f"Query: {selected_query}")

if st.button("Run Query"):
    sql_query = queries[selected_query]
    try:
        result_df = run_query(sql_query)
        st.write("### ✅ Query Result:")
        st.dataframe(result_df)

        # Optional: Download result as CSV
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download as CSV", csv, "query_result.csv", "text/csv")

    except Exception as e:
        st.error(f"Error running query: {e}")
