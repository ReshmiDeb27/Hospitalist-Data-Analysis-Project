# import libraries
import sys
import pandas as pd
from datetime import datetime

# Input file paths
person_path = sys.argv[1]
encounter_path = sys.argv[2]
outcome_path = sys.argv[3]
output_path = sys.argv[4]

# Load datasets
df_person = pd.read_csv(person_path)
df_encounter = pd.read_csv(encounter_path)
df_outcome = pd.read_csv(outcome_path)

# Convert date columns to datetime
df_person['birth_date'] = pd.to_datetime(df_person['birth_date'])
df_encounter['admission_date'] = pd.to_datetime(df_encounter['admit_dt_tm'])
df_encounter['discharge_date'] = pd.to_datetime(df_encounter['discharge_dt_tm'])

# Merge datasets on ENCOUNTER_ID
df_merged = df_person.merge(df_encounter, on='ENCOUNTER_ID', how='left')
df_merged = df_merged.merge(df_outcome, on='ENCOUNTER_ID', how='left')

# Example processing: count number of patients by discharge disposition
summary = df_merged['DISCHARGE_DISPOSITION'].value_counts().reset_index()
summary.columns = ['Discharge Disposition', 'Count']

# Calculate fields
df_merged['age'] = (df_merged['admission_date'] - df_merged['birth_date']).dt.days // 365
df_merged['length_of_stay'] = (df_merged['discharge_date'] - df_merged['admission_date']).dt.days

# Create age groups
df_merged['age_group'] = pd.cut(df_merged['age'], bins=[0, 18, 35, 50, 65, 80, 100],
                                labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81+'], right=False)

# Monthly admission period
df_merged['admit_month'] = df_merged['admission_date'].dt.to_period('M')

# Summary table: Avg LOS by age group and gender per month
summary = df_merged.groupby(['admit_month', 'GENDER', 'age_group'])['length_of_stay'].mean().reset_index()
summary.rename(columns={'length_of_stay': 'avg_length_of_stay'}, inplace=True)

# Export outputs
df_merged.to_csv('output/cleaned_patient_data.csv', index=False)
summary.to_csv('output/los_summary_by_demo.csv', index=False)

print("Data processing complete. Outputs saved to /output folder.")
