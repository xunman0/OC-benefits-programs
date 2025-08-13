import streamlit as st
import pandas as pd

# Load the spreadsheet data
df = pd.read_excel("orange_county_benefits_programs.xlsx", engine="openpyxl")

st.title("Orange County Public Assistance Programs Dashboard")

st.sidebar.header("Filter Programs")

# Filter by Program Name
program_names = df['Program Name'].dropna().unique()
selected_program = st.sidebar.selectbox("Select Program Name", ["All"] + list(program_names))

# Filter by Administering Agency
agencies = df['Administering Agency'].dropna().unique()
selected_agency = st.sidebar.selectbox("Select Administering Agency", ["All"] + list(agencies))

# Filter by Eligibility Criteria
criteria_keywords = st.sidebar.text_input("Search Eligibility Criteria")

# Apply filters
filtered_df = df.copy()
if selected_program != "All":
    filtered_df = filtered_df[filtered_df['Program Name'] == selected_program]
if selected_agency != "All":
    filtered_df = filtered_df[filtered_df['Administering Agency'] == selected_agency]
if criteria_keywords:
    filtered_df = filtered_df[filtered_df['Eligibility Criteria'].str.contains(criteria_keywords, case=False, na=False)]

st.subheader("Filtered Programs")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['Program Name']}")
    st.markdown(f"**Administering Agency:** {row['Administering Agency']}")
    st.markdown(f"**Description:** {row['Description']}")
    st.markdown(f"**Application Link:** [{row['Application Link']}]({row['Application Link']})")
    st.markdown(f"**Last Updated:** {row['Last Updated']}")
    st.markdown(f"**Eligibility Criteria:** {row['Eligibility Criteria']}")
    st.markdown(f"**Update Source URLs:** {row['Update Source URLs']}")
    st.markdown("---")
