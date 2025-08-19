import psycopg2
import pandas as pd
import streamlit as st
from psycopg2.extras import execute_values


# --- Database Connection Function ---
def get_connection():
    return psycopg2.connect(
        host=st.secrets["neon"]["host"],
        dbname=st.secrets["neon"]["dbname"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=st.secrets["neon"]["port"],
        sslmode="require"
    )


# --- Function to load CSV into Neon ---
def load_csv_to_neon(csv_path, table_name):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Read CSV
        df = pd.read_csv(csv_path)

        if df.empty:
            print(f"⚠️ {csv_path} is empty, skipping.")
            return

        columns = list(df.columns)
        values = [tuple(x) for x in df.to_numpy()]

        # Insert rows using execute_values (bulk insert)
        insert_query = f"""
        INSERT INTO "{table_name}" ({", ".join([f'"{col}"' for col in columns])})
        VALUES %s
        ON CONFLICT DO NOTHING;
        """

        execute_values(cursor, insert_query, values)
        conn.commit()

        print(f"✅ {csv_path} uploaded to {table_name} successfully!")

    except Exception as e:
        print(f"❌ Error uploading {csv_path}: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


# --- MAIN SCRIPT ---
if __name__ == "__main__":
    datasets = {
        "Providers.csv": "Providers",
        "Receivers.csv": "Receivers",
        "Food_Listings.csv": "Food_Listings",
        "Claims.csv": "Claims"
    }

    for csv_file, table_name in datasets.items():
        load_csv_to_neon(csv_file, table_name)
