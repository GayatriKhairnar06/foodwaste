import os
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

# ====== CONFIG ======
USER = "postgres"
PASSWORD = "Gayu123"
HOST = "localhost"
PORT = "5432"
DATABASE = "food_wastage"
CSV_DIR = "."  # CSV files ka folder (current dir me)
WRITE_MODE = "replace"  # "append" ya "replace"

# Files → Tables mapping
files_tables = {
    "providers_data.csv": "providers",
    "receivers_data.csv": "receivers",
    "food_listings_data.csv": "food_listings",
    "claims_data.csv": "claims"
}

# ====== ENGINE BANANA ======
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# ====== DATABASE CREATE KARNA ======
def ensure_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DATABASE}")
            print(f"✅ Database '{DATABASE}' created!")
        else:
            print(f"ℹ Database '{DATABASE}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to ensure database: {e}")

# ====== CSV UPLOAD FUNCTION ======
def upload_csvs():
    for file, table in files_tables.items():
        file_path = os.path.join(CSV_DIR, file)
        if not os.path.exists(file_path):
            print(f"⚠ Skipping {file} → File not found.")
            continue
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table, engine, if_exists=WRITE_MODE, index=False)

            # SQLAlchemy 2.x compatible query
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()

            print(f"✅ Uploaded {file} → {table} ({count} rows).")
        except Exception as e:
            print(f"❌ Failed to upload {file} → {table}: {e}")

# ====== RUN ======
if __name__ == "__main__":
    ensure_database()
    upload_csvs()
    print("🎯 All files processed!")
