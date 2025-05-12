# Hospitalist Data Analysis Dashboard

## Project Overview
This project is a full-stack data analysis pipeline for hospital patient records. It allows users to process, store, and visualize hospital encounters using a combination of:

- Python for data processing
- MySQL for structured storage
- Streamlit for interactive dashboards
- Bash for automation

It is designed to help hospitalists and care teams analyze patient flow, admission/discharge trends, and length of stay patterns using de-identified healthcare data.

## Scripts
### Database Implementation 
process_data.py, load_data.py
### Bash Shell Automation 
run.sh
### Python Visualization
app.py with Streamlit

# Setup Instructions

## 1. Clone the Repository
git clone https://github.com/ReshmiDeb27/Hospitalist-Data-Analysis-Project.git

cd Hospitalist-Data-Analysis-Project

## 2. Configure MySQL
Create a MySQL database named: hospital_data.db

Update credentials in Scripts/load_to_mysql.py:

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="hospital_data"
)

