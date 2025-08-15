import pandas as pd
import sqlite3
import os

# Database file name
DB_FILE = "data.db"

# CSV file names and the table names to use in SQLite
tables = {
    "Providers.csv": "providers",
    "Receivers.csv": "receivers",
    "Food_Listings.csv": "food_listings",
    "Claims.csv": "claims"
}

def create_database():
    # Connect to SQLite (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    print(f"📦 Connected to SQLite database: {DB_FILE}")

    # Loop through CSVs and load them into tables
    for csv_file, table_name in tables.items():
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"✅ Loaded '{csv_file}' into table '{table_name}' ({len(df)} rows).")
        else:
            print(f"⚠️ File not found: {csv_file}")

    conn.close()
    print("🎯 Database creation completed!")

if __name__ == "__main__":
    create_database()
