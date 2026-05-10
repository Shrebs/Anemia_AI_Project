import streamlit as st


# -------------------------------------------------
# HEMOGLOBIN FUNCTION
# -------------------------------------------------

def check_hemoglobin(hb, gender):

    # Female
    if gender == 0:

        if hb < 12:
            return "Low"

        elif hb <= 15.5:
            return "Normal"

        else:
            return "High"

    # Male
    else:

        if hb < 13.5:
            return "Low"

        elif hb <= 17.5:
            return "Normal"

        else:
            return "High"


# -------------------------------------------------
# RBC FUNCTION
# -------------------------------------------------

def check_rbc(rbc, gender):

    # Female
    if gender == 0:

        if rbc < 4.0:
            return "Low"

        elif rbc <= 5.2:
            return "Normal"

        else:
            return "High"

    # Male
    else:

        if rbc < 4.5:
            return "Low"

        elif rbc <= 5.9:
            return "Normal"

        else:
            return "High"


# -------------------------------------------------
# MCV FUNCTION
# -------------------------------------------------

def check_mcv(mcv):

    if mcv < 80:
        return "Low"

    elif mcv <= 100:
        return "Normal"

    else:
        return "High"


# -------------------------------------------------
# MCH FUNCTION
# -------------------------------------------------

def check_mch(mch):

    if mch < 27:
        return "Low"

    elif mch <= 33:
        return "Normal"

    else:
        return "High"


# -------------------------------------------------
# MCHC FUNCTION
# -------------------------------------------------

def check_mchc(mchc):

    if mchc < 32:
        return "Low"

    elif mchc <= 36:
        return "Normal"

    else:
        return "High"


# -------------------------------------------------
# RDW FUNCTION
# -------------------------------------------------

def check_rdw(rdw):

    if rdw < 11.5:
        return "Low"

    elif rdw <= 14.5:
        return "Normal"

    else:
        return "High"


# -------------------------------------------------
# APP TITLE
# -------------------------------------------------

st.title("AI-Based Anemia Detection System")

st.write("Enter blood parameter values below:")


# -------------------------------------------------
# USER INPUTS
# -------------------------------------------------

gender_option = st.selectbox(
    "Select Gender",
    ["Female", "Male"]
)

# Convert gender into ML encoding
if gender_option == "Female":
    gender = 0
else:
    gender = 1


hemoglobin = st.number_input("Enter Hemoglobin Value")

rbc = st.number_input("Enter RBC Count")

mcv = st.number_input("Enter MCV Value")

mch = st.number_input("Enter MCH Value")

mchc = st.number_input("Enter MCHC Value")

rdw = st.number_input("Enter RDW Value")


# -------------------------------------------------
# SUBMIT BUTTON
# -------------------------------------------------

if st.button("Analyze Report"):

    # Parameter Analysis
    hb_status = check_hemoglobin(hemoglobin, gender)

    rbc_status = check_rbc(rbc, gender)

    mcv_status = check_mcv(mcv)

    mch_status = check_mch(mch)

    mchc_status = check_mchc(mchc)

    rdw_status = check_rdw(rdw)

    
    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    st.subheader("Blood Parameter Analysis")

    st.write("Hemoglobin Status:", hb_status)

    st.write("RBC Status:", rbc_status)

    st.write("MCV Status:", mcv_status)

    st.write("MCH Status:", mch_status)

    st.write("MCHC Status:", mchc_status)

    st.write("RDW Status:", rdw_status)