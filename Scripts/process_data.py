# Import required libraries
import sys
import pandas as pd
import os

# Specify input file paths for loading raw data into the processing pipeline
person_path = sys.argv[1]
encounter_path = sys.argv[2]
outcome_path = sys.argv[3]
output_path = sys.argv[4]

# Check and create the output directory to avoid file write errors during processing
os.makedirs(output_path, exist_ok=True)

# Load input CSV files into DataFrames for processing and analysis
df_person = pd.read_csv(person_path)     
df_encounter = pd.read_csv(encounter_path)  
df_outcome = pd.read_csv(outcome_path)      

# STEP 1: Standardize raw date columns to datetime type for consistency and computation
df_person['BIRTH_DATE'] = pd.to_datetime(df_person['BIRTH_DATE'])
df_encounter['admission_date'] = pd.to_datetime(df_encounter['ADMIT_DT_TM'])
df_encounter['discharge_date'] = pd.to_datetime(df_encounter['DISCHARGE_DT_TM'])

# STEP 2: Merge datasets using ENCOUNTER_ID to combine patient, encounter, and outcome data into a single dataset
df_merged = df_person.merge(df_encounter, on='ENCOUNTER_ID', how='left')
df_merged = df_merged.merge(df_outcome, on='ENCOUNTER_ID', how='left')

# STEP 3: Calculate patient age from birth date and compute length of stay (LOS) from admission and discharge dates
df_merged['age'] = (df_merged['admission_date'] - df_merged['BIRTH_DATE']).dt.days // 365
df_merged['length_of_stay'] = (df_merged['discharge_date'] - df_merged['admission_date']).dt.days

# STEP 4: Create categorical features (e.g., age group, admit month) to support grouped analysis and visualization
df_merged['age_group'] = pd.cut(df_merged['age'],
                                bins=[0, 18, 35, 50, 65, 80, 120],
                                labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81+'],
                                right=False)

df_merged['admit_month'] = df_merged['admission_date'].dt.to_period('M')

# STEP 5: Aggregate LOS summary by gender, age group, and month of admission for trend analysis
los_summary = df_merged.groupby(['admit_month', 'GENDER', 'age_group'])['length_of_stay'] \
                       .mean().reset_index()
los_summary.rename(columns={'length_of_stay': 'avg_length_of_stay'}, inplace=True)

# STEP 6: Save the final cleaned data and LOS summary as CSV files for later use in the pipeline
df_merged.to_csv(os.path.join(output_path, 'cleaned_patient_data.csv'), index=False)
los_summary.to_csv(os.path.join(output_path, 'los_summary_by_demo.csv'), index=False)

print("Data processing complete. Cleaned files saved to:", output_path)
