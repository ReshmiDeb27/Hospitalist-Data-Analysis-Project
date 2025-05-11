#!/bin/bash
set -e

# Step 1: Setup virtual environment
if [ ! -d "../venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv ../venv

# Step 2: Activate virtual environment
source ../venv/bin/activate

# Step 3: Install required Python packages
pip install --quiet -r ../requirements.txt
pip install --upgrade pip

# Step 4: Prepare input and output directories
mkdir -p ../input ../output

# Step 5: Copy CSVs from Data to input
cp ../Data/patient_data.csv/person.csv input/
cp ../Data/patient_data.csv/encounter.csv input/
cp ../Data/patient_data.csv/outcome.csv input/

# Step 6: Run Python script to generate summary data
echo "Running data processing script"
python3 process_data.py ../input/person.csv ../input/encounter.csv ../input/outcome.csv ../output/summary.csv

# Step 6: Load summary.csv to SQL database
echo "Loading summary.csv into database..."
# Example using SQLite for demo purposes
sqlite3 ../hospital.db < ../Scripts/load_data.sql

echo "Data pipeline complete. Launching Streamlit dashboard..."

# Step 7: Run Streamlit dashboard
streamlit run Scripts/app.py


