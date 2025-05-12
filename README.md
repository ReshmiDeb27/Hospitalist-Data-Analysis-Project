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

Update credentials in Scripts/load_data.py:

conn = mysql.connector.connect(

    host="localhost",
    
    user="root",
    
    password="your_password",
    
    database="hospital_data"
    
)

## 3. Run the Full Pipeline
<pre> ```bash chmod +x run.sh

./run.sh``` </pre>

This script will:

Install dependencies

Copy raw CSVs to input folder

Process & clean data via process_data.py

Create and populate MySQL tables via load_data.py

Launch the Streamlit dashboard

## Details of Each Component
### Scripts/process_data.py

This script:

    Loads person.csv, encounter.csv, outcome.csv

    Merges them based on ENCOUNTER_ID

    Calculates derived fields like:

        Length of stay

        Admission month

        Age group

    Outputs the cleaned data to output/summary.csv

### Scripts/load_to_mysql.py

This script:

    Connects to your MySQL server

    Creates tables: PERSON, ENCOUNTER, and OUTCOME

    Loads summary.csv into a new table (e.g., SUMMARY)

    Apply proper schema and datatypes

### app.py

The Streamlit dashboard provides:

    Sidebar filters (age, gender, facility, dates)

    Data Table view

    Charts for average length of stay by age/gender

    Line plots showing admission/discharge trends

### Bash Script: run.sh

#!/bin/bash

# Step 1: Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 2: Create necessary folders
mkdir -p ../input ../output

# Step 3: Copy data files
cp ../Data/person.csv ../input/
cp ../Data/encounter.csv ../input/
cp ../Data/outcome.csv ../input/

# Step 4: Run data processing script
echo "Running data processing script..."
python3 Scripts/process_data.py ../input/person.csv ../input/encounter.csv ../input/outcome.csv ../output/summary.csv

# Step 5: Load processed data into MySQL
echo "Loading data into MySQL..."
python3 Scripts/load_to_mysql.py

# Step 6: Launch dashboard
echo "Launching dashboard..."
streamlit run Dashboard/app.py

