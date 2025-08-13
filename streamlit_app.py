
import streamlit as st
import pandas as pd

# Load the spreadsheet data
df = pd.read_excel("updated_orange_county_benefits_programs.xlsx", engine="openpyxl")

st.set_page_config(page_title="Disability Benefits Eligibility Tool", layout="centered")

st.title("Orange County Disability Benefits Eligibility Tool")

st.markdown("""
This tool helps families determine which public benefits and programs their child or adult child with disabilities may qualify for based on:
- Age group
- Citizenship
- Current benefits
- Employment and income (if 18+)
- Household income (if under 18)
""")

# Step 1: Age Group
st.header("Step 1: Age Group")
age_group = st.selectbox(
    "Select the age group of the individual with disabilities:",
    ["0-2", "3-21", "22+"]
)
# Step 2: Current Benefits and Citizenship
st.header("Step 2: Current Benefits and Citizenship")

current_benefits = st.multiselect(
    "Select any current benefits or programs the individual is receiving:",
    [
        "First Start",
        "First Start Transition",
        "Institutional Deeming",
        "SSI",
        "SSDI",
        "IHSS",
        "WIC",
        "CalFresh",
        "Medi-Cal"
    ]
)

citizenship_status = st.selectbox(
    "Is the individual a U.S. citizen?",
    ["Yes", "No"]
)
# Step 3: Employment and Income (for individuals 18+)
show_income_section = False
individual_income = 0
is_employed = "No"

if age_group == "22+":
    show_income_section = True
elif age_group == "3-21":
    is_18_or_older = st.checkbox("Is the individual 18 or older?")
    if is_18_or_older:
        show_income_section = True

if show_income_section:
    st.header("Step 3: Employment and Income")
    is_employed = st.selectbox("Is the individual employed?", ["Yes", "No"])
    if is_employed == "Yes":
        individual_income = st.number_input("Enter the individual's annual income (USD):", min_value=0)
# Step 4: Parent/Guardian Household Information (for individuals under 18)
household_income = 0
household_size = 1

if age_group in ["0-2", "3-21"] and not (age_group == "3-21" and show_income_section):
    st.header("Step 4: Parent/Guardian Household Information")

    parent_citizenship = st.selectbox(
        "Is the parent or guardian a U.S. citizen?",
        ["Yes", "No"]
    )

    household_income = st.number_input(
        "Enter the total household annual income (USD):",
        min_value=0
    )

    household_size = st.number_input(
        "Enter the total number of people in the household:",
        min_value=1
    )
# Step 5: Eligibility Calculation and Summary Output
if st.button("Check Eligibility"):
    st.header("Eligibility Summary")

    # Calculate FPL
    base_fpl = 15060
    additional_per_person = 5380
    fpl_threshold = base_fpl + additional_per_person * (household_size - 1)
    fpl_percentage = (household_income / fpl_threshold) * 100 if household_income > 0 else 0

    st.markdown(f"**Estimated Federal Poverty Level (FPL):** {fpl_percentage:.1f}%")

    # Prioritized programs
    st.subheader("Primary Programs")
    st.markdown("""
    These are the core programs that many individuals with disabilities may qualify for:
    """)

    if "Medi-Cal" in current_benefits or fpl_percentage <= 138:
        st.markdown("✅ **Medi-Cal** – Based on income and/or disability status.")
    if "IHSS" in current_benefits or ("Medi-Cal" in current_benefits and age_group in ["3-21", "22+"]):
        st.markdown("✅ **IHSS (In-Home Supportive Services)** – Requires Medi-Cal eligibility and functional need.")
    if "SSI" in current_benefits or (age_group in ["3-21", "22+"] and fpl_percentage <= 100):
        st.markdown("✅ **SSI (Supplemental Security Income)** – Based on disability and financial need.")

    # Additional programs
    st.subheader("Other Potentially Eligible Programs")
    for benefit in current_benefits:
        if benefit not in ["Medi-Cal", "IHSS", "SSI"]:
            st.markdown(f"🔹 **{benefit}** – Already receiving or may qualify based on your inputs.")

    if fpl_percentage <= 185:
        st.markdown("🔹 **WIC** – For children under 5 and pregnant individuals in low-income households.")
    if fpl_percentage <= 200:
        st.markdown("🔹 **CalFresh (SNAP)** – Food assistance for low-income individuals and families.")
    if "Institutional Deeming" in current_benefits:
        st.markdown("🔹 **Institutional Deeming Waiver** – May allow Medi-Cal eligibility regardless of parental income.")

    st.markdown("---")
    st.info("This summary is based on general eligibility guidelines. For a full assessment, contact your local Social Services Agency or Regional Center.")
    import io

# Optional: Generate a downloadable summary
if st.button("Download Summary as Text"):
    summary = f"""
    Orange County Disability Benefits Eligibility Summary

    Age Group: {age_group}
    Citizenship: {citizenship}
    Current Benefits: {', '.join(current_benefits) if current_benefits else 'None'}
    Employed: {is_employed}
    Individual Income: ${individual_income:,}
    Household Income: ${household_income:,}
    Household Size: {household_size}
    Estimated FPL: {fpl_percentage:.1f}%

    Primary Programs:
    - Medi-Cal
    - IHSS
    - SSI

    Additional Programs:
    - {', '.join([b for b in current_benefits if b not in ['Medi-Cal', 'IHSS', 'SSI']])}
    """

    st.download_button(
        label="📄 Download Summary",
        data=summary,
        file_name="eligibility_summary.txt",
        mime="text/plain"
    )

# Optional: Reset form (simulated by rerunning the script)
if st.button("Reset Form"):
    st.experimental_rerun()


