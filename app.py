import streamlit as st
import pandas as pd
import altair as alt

st.title("Hospital Patient Analysis Dashboard")

st.write(
    """
    Welcome to the Hospitalist Dashboard.

    This dashboard displays key metrics and insights to help hospitalists and care teams monitor patient flow, evaluate readmission risks, and enhance care delivery. Use the filters to explore trends in length of stay, discharge outcomes, and patient demographics.

    Data is updated regularly to support real-time decision-making and streamline care coordination efforts.
    """
)

# Load data
df = pd.read_csv('/workspaces/Hospitalist-Data-Analysis-Project/output/summary.csv/cleaned_patient_data.csv')

# Sidebar filters
st.sidebar.header('Data Filter')

# Convert admission date to datetime if not already
df['admission_date'] = pd.to_datetime(df['admission_date'], errors='coerce')

# Age Group Filter
age_groups = df['age_group'].dropna().unique()
selected_group = st.sidebar.multiselect("Select Age Group:", age_groups, default=age_groups)

# Facility Filter
available_facilities = df['FACILITY'].dropna().unique()
selected_facilities = st.sidebar.multiselect("Select Facility", available_facilities, default=available_facilities)

# Gender Filter
available_genders = df['GENDER'].dropna().unique()
selected_genders = st.sidebar.multiselect("Select Gender", available_genders, default=available_genders)

# Date Range Filter
min_date = df['admission_date'].min().date()
max_date = df['admission_date'].max().date()
selected_date_range = st.sidebar.date_input(
    "Select Admission Date Range", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)
start_date, end_date = selected_date_range

# Filter DataFrame
filtered_df = df[
    (df['age_group'].isin(selected_group)) &
    (df['FACILITY'].isin(selected_facilities)) &
    (df['GENDER'].isin(selected_genders)) &
    (df['admission_date'].dt.date >= start_date) &
    (df['admission_date'].dt.date <= end_date)
]

# Tabs
tabs = ['Data Table', 'Charts', 'Trend Analysis']
selected_tab = st.radio("Explore the dashboard by selecting a tab", tabs, index=0)

# 1. Data Table Tab
if selected_tab == 'Data Table':
    st.subheader("Filtered Patient Records")
    st.write(f"Showing {len(filtered_df)} records between {start_date} and {end_date}")
    st.dataframe(filtered_df)

# 2. Chart Tab
elif selected_tab == 'Charts':
    st.subheader("Admit Source Breakdown")
    st.metric("Total Patients", len(filtered_df))
    st.metric("Average Length of Stay", round(filtered_df['length_of_stay'].mean(), 2))

    grouped_df = filtered_df.groupby(['age_group', 'GENDER'])['length_of_stay'].mean().reset_index()

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

# 3. Trend Analysis Tab
elif selected_tab == 'Trend Analysis':
    st.subheader("Admission & Discharge Trends")

    df['discharge_date'] = pd.to_datetime(df['discharge_date'], errors='coerce')

    admit_df = df[df['admission_date'].notna()].copy()
    admit_df['event_date'] = admit_df['admission_date'].dt.date
    admit_df['event_type'] = 'Admit'
    admit_df = admit_df[['event_date', 'event_type', 'ENCOUNTER_ID']]

    discharge_df = df[df['discharge_date'].notna()].copy()
    discharge_df['event_date'] = discharge_df['discharge_date'].dt.date
    discharge_df['event_type'] = 'Discharge'
    discharge_df = discharge_df[['event_date', 'event_type', 'ENCOUNTER_ID']]

    trend_df = pd.concat([admit_df, discharge_df])
    trend_df = trend_df.groupby(['event_date', 'event_type'])['ENCOUNTER_ID'].nunique().reset_index()
    trend_df.columns = ['event_date', 'event_type', 'encounter_count']
    trend_df['event_date'] = pd.to_datetime(trend_df['event_date'])

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

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Created by **Reshmi Deb**")
st.divider()
st.markdown("**Healthcare Statistics Dashboard** | Built with Streamlit")
