from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
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
# PDF REPORT FUNCTION
# -------------------------------------------------

def generate_pdf(prediction_text, severity, cause, diet):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []


    title = Paragraph(
        "Clinical Anemia Assessment Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 12))


    elements.append(
        Paragraph(f"<b>AI Prediction:</b> {prediction_text}", styles['BodyText'])
    )

    elements.append(Spacer(1, 10))


    elements.append(
        Paragraph(f"<b>Severity Level:</b> {severity}", styles['BodyText'])
    )

    elements.append(Spacer(1, 10))


    elements.append(
        Paragraph(f"<b>Possible Cause:</b> {cause}", styles['BodyText'])
    )

    elements.append(Spacer(1, 10))


    elements.append(
        Paragraph(f"<b>Diet Recommendation:</b><br/>{diet}", styles['BodyText'])
    )


    doc.build(elements)

    buffer.seek(0)

    return buffer

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------



st.sidebar.title("Clinical Anemia Assessment System")

mode = st.sidebar.radio(
    "Select Analysis Mode",
    ["Blood Report Analysis", "Symptom Checker"]
)


# -------------------------------------------------
# MAIN TITLE
# -------------------------------------------------

st.title("Clinical Anemia Assessment Dashboard")

st.markdown("---")


if mode == "Blood Report Analysis":

    # -------------------------------------------------
    # USER INPUTS
    # -------------------------------------------------
    
    age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    step=1
)

    gender_option = st.selectbox(
        "Select Gender",
        ["Female", "Male"]
    )

    # Convert gender into ML encoding
    if gender_option == "Female":
        gender = 0
    else:
        gender = 1


    st.subheader("Blood Test Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        hemoglobin = st.number_input("Hemoglobin")

        mch = st.number_input("MCH")

    with col2:
        rbc = st.number_input("RBC Count")

        mchc = st.number_input("MCHC")

    with col3:
        mcv = st.number_input("MCV")

        rdw = st.number_input("RDW")


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

        # Possible Cause Analysis
        cause = possible_cause(mcv)

        # Diet Recommendation
        diet = diet_recommendation(severity)

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
        # CLINICAL SUMMARY
        # -------------------------------------------------

        st.subheader("Clinical Summary")

        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            with st.container(border=True):

                st.markdown("### AI Prediction")

                if prediction[0] == 1:
                    st.error("Anemia Detected")
                else:
                    st.success("No Anemia Detected")

        with row1_col2:
            with st.container(border=True):

                st.markdown("### Severity Level")

                if severity == "No Anemia":
                    st.success(severity)

                elif severity == "Mild Anemia":
                    st.warning(severity)

                elif severity == "Moderate Anemia":
                    st.warning(severity)

                else:
                    st.error(severity)


        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            with st.container(border=True):

                st.markdown("### Possible Cause")

                st.info(cause)

        with row2_col2:
            with st.container(border=True):

                st.markdown("### Diet Recommendation")

                st.markdown(diet)
                
                
                
                        # -------------------------------------------------
        # PDF REPORT
        # -------------------------------------------------

        prediction_text = (
            "Anemia Detected"
            if prediction[0] == 1
            else "No Anemia Detected"
        )

        pdf = generate_pdf(
            prediction_text,
            severity,
            cause,
            diet
        )

        st.download_button(
            label="Download Clinical Report",
            data=pdf,
            file_name="anemia_report.pdf",
            mime="application/pdf"
        )
        
        
        
        
        
        
        
        
# =========================================================
# SYMPTOM CHECKER MODE
# =========================================================

elif mode == "Symptom Checker":

    st.subheader("Symptom-Based Anemia Risk Assessment")

    st.write("Select symptoms experienced by the user:")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        step=1
    )


    # -------------------------------------------------
    # SYMPTOM INPUTS
    # -------------------------------------------------

    st.subheader("Select Symptoms")

    col1, col2, col3 = st.columns(3)

    with col1:

        fatigue = st.checkbox("Fatigue")

        weakness = st.checkbox("Weakness")

        dizziness = st.checkbox("Dizziness")

        headache = st.checkbox("Headache")

        pale_skin = st.checkbox("Pale Skin")


    with col2:

        short_breath = st.checkbox("Shortness of Breath")

        rapid_heartbeat = st.checkbox("Rapid Heartbeat")

        cold_hands = st.checkbox("Cold Hands / Feet")

        chest_pain = st.checkbox("Chest Discomfort")

        fainting = st.checkbox("Fainting Sensation")


    with col3:

        hair_fall = st.checkbox("Hair Fall")

        brittle_nails = st.checkbox("Brittle Nails")

        poor_concentration = st.checkbox("Difficulty Concentrating")

        tingling = st.checkbox("Tingling Hands / Feet")

        craving_ice = st.checkbox("Craving Ice")


    # -------------------------------------------------
    # ANALYZE BUTTON
    # -------------------------------------------------

    if st.button("Analyze Symptoms"):


        # -------------------------------------------------
        # SYMPTOM SCORE
        # -------------------------------------------------

        symptom_score = sum([
            fatigue,
            weakness,
            dizziness,
            headache,
            pale_skin,
            short_breath,
            rapid_heartbeat,
            cold_hands,
            chest_pain,
            fainting,
            hair_fall,
            brittle_nails,
            poor_concentration,
            tingling,
            craving_ice
        ])


        # -------------------------------------------------
        # RISK ANALYSIS
        # -------------------------------------------------

        if symptom_score >= 11:

            risk = "High Possible Anemia Risk"

            severity = "Possible Severe Condition"

        elif symptom_score >= 6:

            risk = "Moderate Possible Anemia Risk"

            severity = "Possible Moderate Condition"

        elif symptom_score >= 2:

            risk = "Low Possible Anemia Risk"

            severity = "Possible Mild Condition"

        else:

            risk = "Minimal Anemia Risk"

            severity = "No Significant Symptoms Reported"


        # -------------------------------------------------
        # DISPLAY RESULTS
        # -------------------------------------------------

        st.subheader("Clinical Summary")


        # ---------------- TOP SUMMARY CARDS ---------------- #

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            with st.container(border=True):

                st.markdown("### Risk Assessment")

                st.warning(risk)


        with summary_col2:

            with st.container(border=True):

                st.markdown("### Severity Interpretation")

                st.info(severity)


        # ---------------- FULL WIDTH WARNING ---------------- #

        with st.container(border=True):

            st.markdown("### Medical Advisory")

            st.warning(
                "⚠️ This symptom-based analysis is not a medical diagnosis. "
                "Please consult a healthcare professional and undergo proper blood testing for accurate evaluation."
            )