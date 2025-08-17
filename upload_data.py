import psycopg2
import pandas as pd
import streamlit as st

# --- Database Connection Function ---
def get_connection():
    return psycopg2.connect(
        host=st.secrets["neon"]["host"],
        dbname=st.secrets["neon"]["dbname"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=st.secrets["neon"]["port"]
    )


# --- Function to load CSV into Neon ---
def load_csv_to_neon(csv_path, table_name, columns):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create table dynamically
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            {', '.join([f"{col} TEXT" for col in columns])}
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Read CSV
        df = pd.read_csv(csv_path)

        # Insert rows
        for _, row in df.iterrows():
            cursor.execute(
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
                tuple(row[col] for col in columns)
            )
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
    # Example: Replace with your actual CSV filenames and columns
    datasets = {
        "providers_data.csv": ("providers_data", ["Provider_ID", "Name", "Type","Address","City","Contact"]),
        "receivers_data.csv": ("receivers_data", ["Receiver_ID","Name", "Type", "City","Contact"]),
        "food_listings_data.csv": ("food_listings_data", ["Food_ID", "Food_Name", "Quantity", "Expiry_Date","Provider_ID","Provider_Type","Location","Food_Type","Meal_Type"]),
        "claims_data.csv": ("claims_data", ["Claim_ID", "Food_ID", "Receiver_ID", "Status","Timestamp"])
    }

    for csv_file, (table_name, columns) in datasets.items():
        load_csv_to_neon(csv_file, table_name, columns)
