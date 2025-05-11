## Title

Hospitalist Dashboard: A Data-Driven Tool for Analyzing Patient Flow, Outcomes, and Readmission Risk. 

### ABSTRACT/PURPOSE

The interactive dashboard is developed with the goal of helping the clinical administrators and hospitalists to improve patient care. The dashboard presents understandable overview of patient demographics, length of stay, discharge outcomes, and readmission risks trends, created with the patient data that is similar to EHR-derived csv files. The project facilitates real-time monitoring to support data-driven decision making by combining Bash, MySQL and Python based visualization tool (streamlit). The dashboard provides trends by age group and gender, highlighting patterns in hospital stay durations and outcome distributions that can be used to improve discharge planning and reduce readmission rates.

## PROJECT OBJECTIVES / GOALS

1. Developed a pipeline that can transform, laod and analyze the patient data into a structured database.
2. Built a reproducible Bash-based workflow that runs the pipeline and launches the dashboard.
3. Designed a Streamlit dashboard with python and SQL that visualizes patient statistics, filtered by age group and time range.

### BACKGROUND

The hospitals unplanned readmissions within a few weeks of discharge has been a concern among hospitals due to increasing cost and their impact on patient outcomes. Hence, hospitalists need a timely and easy access to the patients data to improve discharge planning, resource allocation, and care coordination.
The lack of tools to analyze patient-level summary data in a user-friendly interface despite widespread utilization of EHR systems, especially at smaller clinics may hinder timely decision-making. This dashboard bridges that gap using open-source tools.
While commercial systems like Epic and Cerner offer built-in analytics, this project offers a lightweight, modular, and fully open-source alternative tailored for teaching and small research projects. Unlike general-purpose dashboards, this one focuses on key metrics important to hospitalists and supports data filtering by patient age group and date.

## PROJECT COMPONENTS

# Component	             # Script(s) / Files
Database Implementation	 process_data.py, load_data.py
Bash Shell Script	     run.sh
Python Visualization	 app.py (Streamlit dashboard)




### SQL DDL:

```sql
CREATE OR REPLACE TABLE RESHMI_DB.DASHBOARD_DATA.OUTCOME (
    ENCOUNTER_ID VARCHAR(400),
    DISCHARGE_DISPOSITION VARCHAR(80)
);
