#!/bin/bash

# Step 1: Install required Python packages
pip3 install --quiet -r ../requirements.txt
pip3 install --upgrade pip

# Step 2: Prepare input and output directories
mkdir -p ../input ../output

# Step 3: Copy CSVs from Data to input
cp ../Data/person.csv ../input/
cp ../Data/encounter.csv ../input/
cp ../Data/outcome.csv ../input/

# Step 4: Run Python script to generate summary data
echo "Running data processing script"
python3 process_data.py ../input/person.csv ../input/encounter.csv ../input/outcome.csv ../output/summary.csv

# Step 5: Load summary.csv to SQL database
echo "Loading summary.csv into database..."
python3 Scripts/load_data.py

echo "summary.csv successfully loaded into MySQL"

echo "Data pipeline complete. Launching Streamlit dashboard..."

# Step 7: Run Streamlit
cd ..
streamlit run app.py



