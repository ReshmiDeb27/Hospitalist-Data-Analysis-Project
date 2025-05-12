#!/bin/bash

# Step 1: Update pip and install necessary project dependencies from requirements.txt for dashboard
pip3 install -r ../requirements.txt
pip3 install --upgrade pip

# Step 2: Create input/output folders to support data flow and file management
mkdir -p ../input ../output

# Step 3: Place data files in the input path to prepare for analysis
cp ../Data/person.csv ../input/
cp ../Data/encounter.csv ../input/
cp ../Data/outcome.csv ../input/

# Step 4: Run the script in the input files to preprocess raw data and produce cleaned data for further use
echo "Running data processing script"
python3 process_data.py ../input/person.csv ../input/encounter.csv ../input/outcome.csv ../output/summary.csv

# Step 5: Load the cleaned and processed data into the MySQL database for storage and querying
echo "Loading summary.csv into database..."
python3 Scripts/load_data.py

echo "summary.csv successfully loaded into MySQL"

echo "Data pipeline complete. Launching Streamlit dashboard..."

# # Step 6: Launch the interactive dashboard to review metrics and trends
cd ..
streamlit run app.py



