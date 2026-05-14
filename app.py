import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("models/anemia_model.pkl", "rb"))

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
# ANEMIA SEVERITY FUNCTION
# -------------------------------------------------

def anemia_severity(hb, gender):

    # Female
    if gender == 0:

        if hb >= 12:
            return "No Anemia"

        elif hb >= 10:
            return "Mild Anemia"

        elif hb >= 8:
            return "Moderate Anemia"

        else:
            return "Severe Anemia"

    # Male
    else:

        if hb >= 13.5:
            return "No Anemia"

        elif hb >= 11:
            return "Mild Anemia"

        elif hb >= 8:
            return "Moderate Anemia"

        else:
            return "Severe Anemia"
        
        
        
        
        
# -------------------------------------------------
# POSSIBLE CAUSE FUNCTION
# -------------------------------------------------

def possible_cause(mcv):

    if mcv < 80:
        return "Possible Iron Deficiency Anemia"

    elif mcv > 100:
        return "Possible Vitamin B12 / Folate Deficiency"

    else:
        return "Requires Further Clinical Evaluation"
    
    
# -------------------------------------------------
# DIET RECOMMENDATION FUNCTION
# -------------------------------------------------

def diet_recommendation(severity):

    if severity == "Mild Anemia":

        return """
        • Spinach
        • Beetroot
        • Dates
        • Lentils
        • Pomegranate
        """

    elif severity == "Moderate Anemia":

        return """
        • Iron-rich foods
        • Green leafy vegetables
        • Eggs
        • Beans
        • Citrus fruits
        """

    elif severity == "Severe Anemia":

        return """
        • Immediate medical consultation recommended
        • Iron supplements (doctor advised)
        • Nutrient-rich diet
        • Protein-rich foods
        """

    else:

        return """
        • Maintain balanced healthy diet
        • Regular hydration
        • Nutritious meals
        """
    

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

    # Prepare data for ML model
    input_data = np.array([[gender, hemoglobin, mch, mchc, mcv]])

    # AI Prediction
    prediction = model.predict(input_data)
    
    # Severity Analysis
    severity = anemia_severity(hemoglobin, gender)

    

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


    # -------------------------------------------------
    # AI PREDICTION RESULT
    # -------------------------------------------------

    st.subheader("AI Prediction")

    if prediction[0] == 1:
        st.error("Anemia Detected")

    else:
        st.success("No Anemia Detected")
        
        
    # -------------------------------------------------
    # SEVERITY LEVEL
    # -------------------------------------------------

    st.subheader("Severity Level")

    if severity == "No Anemia":
        st.success(severity)

    elif severity == "Mild Anemia":
        st.warning(severity)

    elif severity == "Moderate Anemia":
        st.warning(severity)

    else:
        st.error(severity)
        
        
      # -------------------------------------------------
    # POSSIBLE CAUSE
    # -------------------------------------------------
    
    # Possible Cause Analysis
    cause = possible_cause(mcv)
    
    st.subheader("Possible Cause")

    st.info(cause)   
    
    
    
    
    # -------------------------------------------------
    # DIET RECOMMENDATION
    # -------------------------------------------------

    # Diet Recommendation
    diet = diet_recommendation(severity)
    
    st.subheader("Suggested Diet")

    st.success(diet)
        
        
    