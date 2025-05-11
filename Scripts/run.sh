#!/bin/bash

# Step 3: Install required Python packages
pip3 install --quiet -r ../requirements.txt
pip3 install --upgrade pip

# Step 4: Prepare input and output directories
mkdir -p ../input ../output

# Step 5: Copy CSVs from Data to input
cp ../Data/person.csv ../input/
cp ../Data/encounter.csv ../input/
cp ../Data/outcome.csv ../input/

# Step 6: Run Python script to generate summary data
echo "Running data processing script"
python3 process_data.py ../input/person.csv ../input/encounter.csv ../input/outcome.csv ../output/summary.csv

echo "Data pipeline complete. Launching Streamlit dashboard..."

# Step 7: Run Streamlit
cd ..
streamlit run app.py



