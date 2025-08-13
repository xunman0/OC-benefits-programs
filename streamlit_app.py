import streamlit as st
import pandas as pd

# Load the spreadsheet data
df = pd.read_excel("orange_county_benefits_programs.xlsx", engine="openpyxl")

st.title("Orange County Public Assistance Eligibility Finder")

st.markdown("Fill out the form below to see which programs you may be eligible for based on your household information.")

# Form for user input
with st.form("eligibility_form"):
    household_income = st.number_input("Household Annual Income (USD)", min_value=0)
    household_size = st.number_input("Number of Household Members", min_value=1)
    num_disabled_children = st.number_input("Number of Children with Disabilities", min_value=0)
    pregnant = st.selectbox("Is anyone in the household pregnant?", ["No", "Yes"])
    employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Disabled", "Student"])
    veteran_status = st.selectbox("Is anyone a veteran?", ["No", "Yes"])
    receives_ssi = st.selectbox("Receiving SSI?", ["No", "Yes"])
    receives_snap = st.selectbox("Receiving SNAP (CalFresh)?", ["No", "Yes"])
    receives_medical = st.selectbox("Receiving Medi-Cal?", ["No", "Yes"])
    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    base_fpl = 15060
    additional_per_person = 5380
    fpl_threshold = base_fpl + additional_per_person * (household_size - 1)
    fpl_percentage = (household_income / fpl_threshold) * 100

    st.markdown(f"### Estimated FPL: {fpl_percentage:.1f}%")

    matching_programs = []

    for _, row in df.iterrows():
        criteria = str(row.get("Eligibility Criteria", "")).lower()
        match = False

        if "ssi" in criteria and receives_ssi == "Yes":
            match = True
        elif "snap" in criteria and receives_snap == "Yes":
            match = True
        elif "medi-cal" in criteria and receives_medical == "Yes":
            match = True
        elif "pregnant" in criteria and pregnant == "Yes":
            match = True
        elif "veteran" in criteria and veteran_status == "Yes":
            match = True
        elif "disabilities" in criteria and num_disabled_children > 0:
            match = True
        elif "unemployed" in criteria and employment_status == "Unemployed":
            match = True
        elif "student" in criteria and employment_status == "Student":
            match = True
        elif "disabled" in criteria and employment_status == "Disabled":
            match = True
        elif "income" in criteria or "fpl" in criteria:
            if fpl_percentage <= 400:
                match = True

        if match:
            matching_programs.append(row)

    if matching_programs:
        st.subheader("Programs You May Be Eligible For")
        for program in matching_programs:
            st.markdown(f"### {program['Program Name']}")
            st.markdown(f"**Administering Agency:** {program['Administering Agency']}")
            st.markdown(f"**Description:** {program['Description']}")
            st.markdown(f"**Application Link:** [{program['Application Link']}]({program['Application Link']})")
            st.markdown(f"**Last Updated:** {program['Last Updated']}")
            st.markdown(f"**Eligibility Criteria:** {program['Eligibility Criteria']}")
            st.markdown(f"**Update Source URLs:** {program['Update Source URLs']}")
            st.markdown("---")
    else:
        st.warning("No matching programs found based on the provided information.")
