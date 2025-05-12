import streamlit as st
import pandas as pd
import altair as alt

# Display the main dashboard title at the top of the page
st.title("Hospital Patient Analysis Dashboard")

# Add an introductory paragraph explaining the dashboard’s purpose
st.write(
    """
    Welcome to the Hospitalist Dashboard.

    This dashboard displays key metrics and insights to help hospitalists and care teams monitor patient flow, evaluate readmission risks, and enhance care delivery. Use the filters to explore trends in length of stay, discharge outcomes, and patient demographics.

    Data is updated regularly to support real-time decision-making and streamline care coordination efforts.
    """
)

# Load the data from a CSV file
# This file contains cleaned, de-identified patient records for analysis
df = pd.read_csv('/workspaces/Hospitalist-Data-Analysis-Project/output/summary.csv/cleaned_patient_data.csv')

# Sidebar filters to customize data views based on user preferences
st.sidebar.header('Data Filter')

# Convert the admission_date column to datetime format to support accurate date-based filtering
df['admission_date'] = pd.to_datetime(df['admission_date'], errors='coerce')

# Create a dropdown to filter data by age group 
# To support age-specific trends in length of stay and outcomes.
age_groups = df['age_group'].dropna().unique()
selected_group = st.sidebar.multiselect("Select Age Group:", age_groups, default=age_groups)

# Create a dropdown to filter data by facility 
# to allow users to compare patient outcomes and trends across different hospital locations
available_facilities = df['FACILITY'].dropna().unique()
selected_facilities = st.sidebar.multiselect("Select Facility", available_facilities, default=available_facilities)

# Create a dropdown to filter data by gender 
# to help analyze patient metrics and outcomes across male and female populations
available_genders = df['GENDER'].dropna().unique()
selected_genders = st.sidebar.multiselect("Select Gender", available_genders, default=available_genders)

# Use a date range filter to explore how metrics vary across different time intervals
min_date = df['admission_date'].min().date()
max_date = df['admission_date'].max().date()
selected_date_range = st.sidebar.date_input(
    "Select Admission Date Range", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)
start_date, end_date = selected_date_range

# Filter the dataset using the selected age group, facility, gender, and admission date range criteria
filtered_df = df[
    (df['age_group'].isin(selected_group)) &
    (df['FACILITY'].isin(selected_facilities)) &
    (df['GENDER'].isin(selected_genders)) &
    (df['admission_date'].dt.date >= start_date) &
    (df['admission_date'].dt.date <= end_date)
]

# Create tabs to organize dashboard content into separate views (Data Table, Charts, and Trend Analysis)
tabs = ['Data Table', 'Charts', 'Trend Analysis']
selected_tab = st.radio("Explore the dashboard by selecting a tab", tabs, index=0)

# TAB 1: Show the raw patient data after applying all filters in a table
if selected_tab == 'Data Table':
    st.subheader("Filtered Patient Records")
    st.write(f"Showing {len(filtered_df)} records between {start_date} and {end_date}")
    st.dataframe(filtered_df)

# TAB 2: Visualize key metrics using bar charts reflecting the current filter selections
elif selected_tab == 'Charts':
    st.subheader("Admit Source Breakdown")

 # Output basic summary figures such as patient count and average LOS for current filters   
    st.metric("Total Patients", len(filtered_df))
    st.metric("Average Length of Stay", round(filtered_df['length_of_stay'].mean(), 2))

# Group the filtered data by age group and gender to calculate the average length of stay
    grouped_df = filtered_df.groupby(['age_group', 'GENDER'])['length_of_stay'].mean().reset_index()

# Visualize aggregated metrics using a bar chart created with Altair
    Bar_plot = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('age_group:N', title='Age Group'),
        y=alt.Y('length_of_stay:Q', title='Avg Length of Stay'),
        color=alt.Color('GENDER:N', title='Gender'),
        column=alt.Column('GENDER:N', title='Gender')
    ).properties(
        width=200,
        height=400,
        title="Average Length of Stay by Age Group and Gender"
    )
    st.altair_chart(Bar_plot)

# TAB 3: Display line charts showing daily trends in admissions and discharges
elif selected_tab == 'Trend Analysis':
    st.subheader("Admission & Discharge Trends")

# Standardize discharge_date column to datetime for consistent date handling
    df['discharge_date'] = pd.to_datetime(df['discharge_date'], errors='coerce')

# Filter the dataset to include only records with valid admission dates
    admit_df = df[df['admission_date'].notna()].copy()
    admit_df['event_date'] = admit_df['admission_date'].dt.date
    admit_df['event_type'] = 'Admit'
    admit_df = admit_df[['event_date', 'event_type', 'ENCOUNTER_ID']]

# Filter the dataset to include only records with valid discharge dates
    discharge_df = df[df['discharge_date'].notna()].copy()
    discharge_df['event_date'] = discharge_df['discharge_date'].dt.date
    discharge_df['event_type'] = 'Discharge'
    discharge_df = discharge_df[['event_date', 'event_type', 'ENCOUNTER_ID']]

# Combine admission and discharge records to support combined trend visualizations
    trend_df = pd.concat([admit_df, discharge_df])
    trend_df = trend_df.groupby(['event_date', 'event_type'])['ENCOUNTER_ID'].nunique().reset_index()
    trend_df.columns = ['event_date', 'event_type', 'encounter_count']
    trend_df['event_date'] = pd.to_datetime(trend_df['event_date'])

# Visualize trends in admissions and discharges using a line chart
    chart = alt.Chart(trend_df).mark_line(point=True).encode(
        x=alt.X('event_date:T', title='Date'),
        y=alt.Y('encounter_count:Q', title='Encounter Count'),
        color=alt.Color('event_type:N', title='Event Type'),
        tooltip=['event_date:T', 'event_type:N', 'encounter_count:Q']
    ).properties(
        width=700,
        height=400,
        title="Admission & Discharge Trends Over Time"
    )
    st.altair_chart(chart)

# Include footer with author name and tool acknowledgment
st.sidebar.markdown("---")
st.sidebar.markdown("Created by **Reshmi Deb**")
st.divider()
st.markdown("**Healthcare Statistics Dashboard** | Built with Streamlit")
