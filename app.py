import streamlit as st
import pandas as pd
import altair as alt

st.title("🏥 Hospital Patient Analysis Dashboard")

st.write(
    """
    Welcome to the Hospitalist Dashboard.

    This dashboard displays key metrics and insights to help hospitalists and care teams monitor patient flow, evaluate readmission risks, and enhance care delivery. Use the filters to explore trends in length of stay, discharge outcomes, and patient demographics.

    Data is updated regularly to support real-time decision-making and streamline care coordination efforts.
    """
)

#Tabs

tabs = ['Data Table', 'Charts', 'Relationship Analysis', 'Trend Analysis']
selected_tab = st.radio("Explore the dashboard by selecting a tab", tabs, index=0)

# Load data
df = pd.read_csv('/workspaces/Hospitalist-Data-Analysis-Project/output/summary.csv/cleaned_patient_data.csv')

# Sidebar filters
st.sidebar.header('Data Filter')
st.sidebar.header("Filters")
age_groups = df['age_group'].unique()
selected_group = st.sidebar.multiselect("Select Age Group:", age_groups, default=age_groups)
filtered_df = df[df['age_group'].isin(selected_group)]

# Convert admission date to datetime if not already
df['admission_date'] = pd.to_datetime(df['admission_date'], errors='coerce')

# 1. Select Facility
available_facilities = df['FACILITY'].dropna().unique()
selected_facilities = st.sidebar.multiselect("Select Facility", available_facilities, default=available_facilities)

# 2. Select Date Range
min_date = df['admission_date'].min().date()
max_date = df['admission_date'].max().date()
selected_date_range = st.sidebar.date_input(
    "Select Admission Date Range", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)

# Filter the data
df_filtered = df[
    (df['FACILITY'].isin(selected_facilities)) &
    (df['admission_date'].dt.date >= selected_date_range[0]) &
    (df['admission_date'].dt.date <= selected_date_range[1])
]
# Set date range
start_date, end_date = selected_date_range

# 1. Select Gender (Multi-Select Dropdown)
available_genders = df['GENDER'].dropna().unique()
selected_genders = st.sidebar.multiselect("Select Gender", available_genders, default=available_genders)

# Filter the DataFrame based on selected genders
filtered_df = filtered_df[filtered_df['GENDER'].isin(selected_genders)]


# 1. Data Table Tab

if selected_tab == 'Data Table':
    st.subheader("Filtered Patient Records")
    st.write(f"Showing {len(df_filtered)} records between {start_date} and {end_date}")
    st.dataframe(df_filtered)

# 2. Charts Tab

elif selected_tab == 'Charts':
    st.subheader("Admit Source Breakdown")

    # Show metrics
    st.metric("Total Patients", len(filtered_df))
    st.metric("Average Length of Stay", round(filtered_df['length_of_stay'].mean(), 2))

    # Prepare data for chart (average length of stay by age group and gender)
grouped_df = filtered_df.groupby(['age_group', 'GENDER'])['length_of_stay'].mean().reset_index()

    # Chart
chart = alt.Chart(grouped_df).mark_bar().encode(
    x=alt.X('age_group:N', title='Age Group'),
    y=alt.Y('length_of_stay:Q', title='Avg Length of Stay'),
    color=alt.Color('GENDER:N', title='GENDER'),
    column=alt.Column('GENDER:N', title='GENDER')  # Optional: separate columns for gender
).properties(
    width=200,
    height=400,
    title="Average Length of Stay by Age Group and Gender"
)

st.altair_chart(chart)

