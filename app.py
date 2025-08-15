import streamlit as st
import psycopg2
import pandas as pd


# Function to get a database connection using st.secrets
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["neon"]["ep-green-base-a1qymscb-pooler.ap-southeast-1.aws.neon.tech"],
            dbname=st.secrets["neon"]["food_wastage"],
            user=st.secrets["neon"]["neondb_owner"],
            password=st.secrets["neon"]["npg_fFN8DhKjq6wM"],
            port=st.secrets["neon"]["5432"]
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None


# --- Main Streamlit App ---

st.title("Food Wastage Management Dashboard 🥭")

# Get database connection
conn = get_db_connection()

if conn:
    st.success("Successfully connected to Neon database!")
    cursor = conn.cursor()

    try:
        # Create a sample table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS providers (
            provider_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            contact VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        st.info("Ensured 'providers' table exists.")

        # Insert some sample data to avoid an empty table
        # Use ON CONFLICT DO NOTHING to avoid duplicate entries on each run
        insert_query = """
        INSERT INTO providers (name, city, contact) VALUES
        ('Green Plate', 'New York', '123-456-7890'),
        ('The Daily Spoon', 'Los Angeles', '098-765-4321'),
        ('The Daily Spoon', 'Los Angeles', '098-765-4321')
        ON CONFLICT DO NOTHING;
        """
        cursor.execute(insert_query)
        conn.commit()
        st.info("Inserted sample data (if not already present).")

        # --- SQL Query Example ---
        st.header("Food Providers by City")

        # Get the list of cities from the database to populate a selectbox
        cursor.execute("SELECT DISTINCT city FROM providers ORDER BY city;")
        cities = [row[0] for row in cursor.fetchall()]

        selected_city = st.selectbox("Select a city:", cities)

        # Query to fetch providers for the selected city
        query = f"SELECT name, city, contact FROM providers WHERE city = '{selected_city}';"
        df = pd.read_sql(query, conn)

        # Display the results
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning(f"No providers found in {selected_city}.")

    except Exception as e:
        st.error(f"An error occurred during database operations: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()
            st.write("Connection closed.")