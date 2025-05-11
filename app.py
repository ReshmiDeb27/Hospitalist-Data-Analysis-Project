import streamlit as st
import pandas as pd
import altair as alt

st.title("🏥 Hospital Patient Analysis Dashboard")

df = pd.read_csv('/workspaces/Hospitalist-Data-Analysis-Project/output/summary.csv/cleaned_patient_data.csv')

# Sidebar filters
age_groups = df['age_group'].unique()
selected_group = st.sidebar.multiselect("Select Age Group:", age_groups, default=age_groups)

filtered_df = df[df['age_group'].isin(selected_group)]

# Show metrics
st.metric("Total Patients", len(filtered_df))
st.metric("Average Length of Stay", round(filtered_df['length_of_stay'].mean(), 2))

# Chart
chart = alt.Chart(filtered_df).mark_bar().encode(
    x='age_group:N',
    y='length_of_stay:Q',
    color='gender:N'
).properties(
    width=600,
    height=400,
    title="Average Length of Stay by Age Group and Gender"
)

st.altair_chart(chart)
