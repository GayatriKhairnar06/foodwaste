import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Build DATABASE_URL dynamically from Streamlit secrets
DATABASE_URL = (
    f"postgresql+psycopg2://{st.secrets['neon']['user']}:"
    f"{st.secrets['neon']['password']}@"
    f"{st.secrets['neon']['host']}:"
    f"{st.secrets['neon']['port']}/"
    f"{st.secrets['neon']['dbname']}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
