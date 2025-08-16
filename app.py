import streamlit as st
import psycopg2
import pandas as pd

# Function to get a database connection using st.secrets
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

        # Insert some sample data (with ON CONFLICT DO NOTHING)
        insert_query = """
        INSERT INTO providers (name, city, contact) VALUES
        ('Green Plate', 'New York', '123-456-7890'),
        ('The Daily Spoon', 'Los Angeles', '098-765-4321')
        ON CONFLICT DO NOTHING;
        """
        cursor.execute(insert_query)
        conn.commit()
        st.info("Inserted sample data (if not already present).")

        # --- SQL Query Example ---
        st.header("Food Providers by City")

        # Get list of cities
        cursor.execute("SELECT DISTINCT city FROM providers ORDER BY city;")
        cities = [row[0] for row in cursor.fetchall()]

        if cities:
            selected_city = st.selectbox("Select a city:", cities)

            # Fetch providers for the selected city
            query = "SELECT name, city, contact FROM providers WHERE city = %s;"
            df = pd.read_sql(query, conn, params=(selected_city,))

            if not df.empty:
                st.dataframe(df)
            else:
                st.warning(f"No providers found in {selected_city}.")
        else:
            st.warning("No cities found in database.")

    except Exception as e:
        st.error(f"An error occurred during database operations: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            st.write("Connection closed.")
