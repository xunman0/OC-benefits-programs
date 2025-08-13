
import streamlit as st
import pandas as pd

# Load the spreadsheet data
df = pd.read_excel("updated_orange_county_benefits_programs.xlsx", engine="openpyxl")

st.title("Orange County Disability Benefits Eligibility Finder")

st.markdown("This form helps families determine which programs an individual with disabilities may qualify for based on age, income, citizenship, and other factors.")

# Section: Family Information
st.header("Family Information (Parent/Guardian)")
with st.form("family_info"):
    household_income = st.number_input("Household Annual Income (USD)", min_value=0)
    household_size = st.number_input("Number of Household Members", min_value=1)
    parent_citizenship = st.selectbox("Parent/Guardian Citizenship Status", ["U.S. Citizen", "Lawful Permanent Resident", "Other"])
    submitted_family = st.form_submit_button("Continue to Individual Section")

if submitted_family:
    st.session_state["household_income"] = household_income
    st.session_state["household_size"] = household_size
    st.session_state["parent_citizenship"] = parent_citizenship

# Section: Individual with Disability
if submitted_family:
    st.header("Individual with Disability")
    with st.form("individual_info"):
        age = st.number_input("Age of Individual", min_value=0)
        disability_type = st.text_input("Type of Disability")
        receives_ssi = st.selectbox("Receiving SSI?", ["No", "Yes"])
        receives_medical = st.selectbox("Receiving Medi-Cal?", ["No", "Yes"])
        receives_snap = st.selectbox("Receiving SNAP (CalFresh)?", ["No", "Yes"])
        child_citizenship = st.selectbox("Individual's Citizenship Status", ["U.S. Citizen", "Lawful Permanent Resident", "Other"])
        regional_center_client = st.selectbox("Is the individual a Regional Center client?", ["No", "Yes"])
        if age >= 18:
            employed = st.selectbox("Is the individual employed?", ["No", "Yes"])
            individual_income = st.number_input("Individual's Annual Income (USD)", min_value=0) if employed == "Yes" else 0
        else:
            employed = "No"
            individual_income = 0
        submitted_individual = st.form_submit_button("Check Eligibility")

    if submitted_individual:
        base_fpl = 15060
        additional_per_person = 5380
        fpl_threshold = base_fpl + additional_per_person * (st.session_state["household_size"] - 1)
        fpl_percentage = (st.session_state["household_income"] / fpl_threshold) * 100

        st.subheader(f"Estimated Federal Poverty Level (FPL): {fpl_percentage:.1f}%")

        matching_programs = []

        for _, row in df.iterrows():
            criteria = str(row.get("Eligibility Criteria", "")).lower()
            match = False

            if "ssi" in criteria and receives_ssi == "yes":
                match = True
            elif "medi-cal" in criteria and receives_medical == "yes":
                match = True
            elif "snap" in criteria and receives_snap == "yes":
                match = True
            elif "regional center" in criteria and regional_center_client == "yes":
                match = True
            elif "citizenship" in criteria and child_citizenship.lower() in criteria:
                match = True
            elif "income" in criteria or "fpl" in criteria:
                if fpl_percentage <= 400 or individual_income <= 25000:
                    match = True
            elif "age" in criteria:
                if age <= 2 and "0-2" in criteria:
                    match = True
                elif 3 <= age <= 21 and "3-21" in criteria:
                    match = True
                elif age >= 22 and "22+" in criteria:
                    match = True

            if match:
                matching_programs.append(row)

        # Prioritize Medi-Cal, IHSS, SSI
        priority_programs = []
        other_programs = []
        for program in matching_programs:
            name = program['Program Name'].lower()
            if "medi-cal" in name or "ihss" in name or "ssi" in name:
                priority_programs.append(program)
            else:
                other_programs.append(program)

        st.subheader("Eligibility Summary")

        if priority_programs:
            st.markdown("### Priority Programs (Medi-Cal, IHSS, SSI)")
            for program in priority_programs:
                st.markdown(f"**{program['Program Name']}**")
                st.markdown(f"- Administering Agency: {program['Administering Agency']}")
                st.markdown(f"- Description: {program['Description']}")
                st.markdown(f"- Application Link: [{program['Application Link']}]({program['Application Link']})")
                st.markdown(f"- Eligibility Criteria: {program['Eligibility Criteria']}")
                st.markdown("---")

        if other_programs:
            st.markdown("### Additional Eligible Programs")
            for program in other_programs:
                st.markdown(f"**{program['Program Name']}**")
                st.markdown(f"- Administering Agency: {program['Administering Agency']}")
                st.markdown(f"- Description: {program['Description']}")
                st.markdown(f"- Application Link: [{program['Application Link']}]({program['Application Link']})")
                st.markdown(f"- Eligibility Criteria: {program['Eligibility Criteria']}")
                st.markdown("---")

        if not matching_programs:
            st.warning("No matching programs found based on the provided information.")
