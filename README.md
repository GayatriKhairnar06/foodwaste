🍴 Food Waste Management System

## 📌 Overview
The **Food Waste Management System** is a web-based platform built with **Streamlit** and **PostgreSQL (Neon DB)** to minimize food wastage by connecting **food providers** (restaurants, caterers, NGOs, etc.) 
with **receivers** (charity organizations, individuals in need).  
The platform provides:
- Food listing & claims management  
- Receiver–provider matching  
- Data upload via CSV    
- Dashboard for querying and filtering  

## 🏗️ Project Structure
Food Waste Management/
│── api.py # Streamlit app exposing APIs for CRUD & queries
│── crud.py # Contains create, read, update, delete functions
│── upload_data.py # Script to upload CSV data into Neon DB
│── queries.sql # SQL scripts for creating tables & running queries
│── schemas.py # Pydantic models for request/response validation
│── requirements.txt # Python dependencies
│── README.md # Project documentation
│── /data # Folder containing sample CSV datasets

## ⚙️ Tech Stack
- Frontend/UI: Streamlit  
- Backend: Python (FastAPI/Streamlit APIs + CRUD logic)  
- Database: PostgreSQL (Neon Cloud DB)  
- ORM/Validation: psycopg2 + Pydantic  
- Deployment: Streamlit Cloud  

## 🚀 Features
- Upload CSV files directly to database  
- Manage Providers, Receivers, Food Listings, and Claims  
- Filter results dynamically in UI  
- Contact providers directly through displayed details  
- Prevents duplicate records with `ON CONFLICT DO NOTHING`  

## 🔑 Database Schema
Main tables:
- Providers → Stores provider details  
- Receivers → Stores receiver details  
- Food_Listings → Stores available food info  
- Claims → Tracks claims of food by receivers  

## 📂 Setup Instructions
1. Clone the repo
  git clone https://github.com/your-username/food-waste-management.git
  cd food-waste-management
2. Install dependencies
  pip install -r requirements.txt
3. Configure database
  Create a .streamlit/secrets.toml file:
  [neon]
  host = "your-neon-host"
  dbname = "your-dbname"
  user = "your-username"
  password = "your-password"
  port = 5432
4. Run database migrations
    psql -h your-neon-host -U your-username -d your-dbname -f queries.sql
5. Upload data
  python upload_data.py
6. Run Streamlit app
    streamlit run api.py
## 📊 Example Query (Streamlit UI)
Filter food listings by city, provider, food type, meal type
Show contact details of providers for coordination
## ✅ Future Enhancements
Authentication for providers & receivers
Notification system (email/SMS) for food availability
Analytics dashboard with food wastage statistics
AI-based prediction of surplus food
