import streamlit as st
import pandas as pd

# Load the spreadsheet data
df = pd.read_excel("orange_county_benefits_programs.xlsx", engine="openpyxl")

st.title("Orange County Public Assistance Eligibility Finder")

st.markdown("Use this form to determine which programs your family or individual with disabilities may be eligible for. Questions are categorized to distinguish between parent/guardian and the individual with disabilities age 18+.")

# Form for user input
with st.form("eligibility_form"):
    st.header("Family Information (Parent/Guardian)")
    family_income = st.number_input("Parent/Guardian Annual Household Income (USD)", min_value=0)
    household_size = st.number_input("Total Number of Household Members", min_value=1)
    receives_snap = st.selectbox("Is the household receiving SNAP (CalFresh)?", ["No", "Yes"])
    receives_medical = st.selectbox("Is the household receiving Medi-Cal?", ["No", "Yes"])

    st.header("Individual with Disability")
    individual_age = st.number_input("Age of Individual with Disability", min_value=0)
    individual_disabled = st.selectbox("Does the individual have a documented disability?", ["No", "Yes"])
    individual_rc_client = st.selectbox("Is the individual a Regional Center client?", ["No", "Yes"])
    individual_pregnant = st.selectbox("Is the individual pregnant?", ["No", "Yes"])
    individual_employment_status = st.selectbox("Individual's Employment Status", ["Employed", "Unemployed", "Disabled", "Student"])
    individual_veteran_status = st.selectbox("Is the individual a veteran?", ["No", "Yes"])
    receives_ssi = st.selectbox("Is the individual receiving SSI?", ["No", "Yes"])

    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    base_fpl = 15060
    additional_per_person = 5380
    fpl_threshold = base_fpl + additional_per_person * (household_size - 1)
    fpl_percentage = (family_income / fpl_threshold) * 100

    st.markdown(f"### Estimated Federal Poverty Level (FPL): {fpl_percentage:.1f}%")

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
        elif "pregnant" in criteria and individual_pregnant == "Yes":
            match = True
        elif "veteran" in criteria and individual_veteran_status == "Yes":
            match = True
        elif "disabilities" in criteria and individual_disabled == "Yes":
            match = True
        elif "regional center" in criteria and individual_rc_client == "Yes":
            match = True
        elif "unemployed" in criteria and individual_employment_status == "Unemployed":
            match = True
        elif "student" in criteria and individual_employment_status == "Student":
            match = True
        elif "disabled" in criteria and individual_employment_status == "Disabled":
            match = True
        elif "income" in criteria or "fpl" in criteria:
            if fpl_percentage <= 400:
                match = True
        elif "age 0-2" in criteria and individual_age <= 2:
            match = True
        elif "age 3-21" in criteria and 3 <= individual_age <= 21:
            match = True
        elif "age 22+" in criteria and individual_age >= 22:
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
