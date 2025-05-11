# Import required libraries
import sys
import pandas as pd
import os

# Input file paths
person_path = sys.argv[1]
encounter_path = sys.argv[2]
outcome_path = sys.argv[3]
output_path = sys.argv[4]

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Load input CSV files
df_person = pd.read_csv(person_path)     # Expects: PATIENT_ID, ENCOUNTER_ID, BIRTH_DATE, GENDER, PATIENT_TYPE
df_encounter = pd.read_csv(encounter_path)  # Expects: ENCOUNTER_ID, FACILITY, UNIT, ADMIT_SOURCE, ADMIT_DT_TM, DISCHARGE_DT_TM
df_outcome = pd.read_csv(outcome_path)      # Expects: ENCOUNTER_ID, DISCHARGE_DISPOSITION

# ------------------------------------------
# 🧼 STEP 1: Format dates to datetime objects
# ------------------------------------------
df_person['BIRTH_DATE'] = pd.to_datetime(df_person['BIRTH_DATE'])
df_encounter['admission_date'] = pd.to_datetime(df_encounter['ADMIT_DT_TM'])
df_encounter['discharge_date'] = pd.to_datetime(df_encounter['DISCHARGE_DT_TM'])

# ------------------------------------------
# 🔗 STEP 2: Merge datasets on ENCOUNTER_ID
# ------------------------------------------
df_merged = df_person.merge(df_encounter, on='ENCOUNTER_ID', how='left')
df_merged = df_merged.merge(df_outcome, on='ENCOUNTER_ID', how='left')

# ------------------------------------------------------
# 🧮 STEP 3: Calculate patient age and length of stay (LOS)
# ------------------------------------------------------
df_merged['age'] = (df_merged['admission_date'] - df_merged['BIRTH_DATE']).dt.days // 365
df_merged['length_of_stay'] = (df_merged['discharge_date'] - df_merged['admission_date']).dt.days

# ------------------------------------------------------
# 🎯 STEP 4: Create categorical features for analysis
# ------------------------------------------------------
df_merged['age_group'] = pd.cut(df_merged['age'],
                                bins=[0, 18, 35, 50, 65, 80, 120],
                                labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81+'],
                                right=False)

df_merged['admit_month'] = df_merged['admission_date'].dt.to_period('M')

# ----------------------------------------------------------------
# 📊 STEP 5: LOS summary by gender, age group, and admission month
# ----------------------------------------------------------------
los_summary = df_merged.groupby(['admit_month', 'GENDER', 'age_group'])['length_of_stay'] \
                       .mean().reset_index()

los_summary.rename(columns={'length_of_stay': 'avg_length_of_stay'}, inplace=True)

# -----------------------------------------------------
# 💾 STEP 6: Save cleaned data and summary to CSV files
# -----------------------------------------------------
df_merged.to_csv(os.path.join(output_path, 'cleaned_patient_data.csv'), index=False)
los_summary.to_csv(os.path.join(output_path, 'los_summary_by_demo.csv'), index=False)

print("✅ Data processing complete. Cleaned files saved to:", output_path)
