from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

import streamlit as st
import pickle
import numpy as np


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Clinical Anemia Assessment",
    page_icon="🩸",
    layout="wide"
)


# =========================================================
# PROFESSIONAL CLINICAL UI
# =========================================================

st.markdown("""
<style>

/* ---------- MAIN APP ---------- */

.stApp {
    background-color: #f4f7fb;
    font-family: 'Segoe UI', sans-serif;
}


/* ---------- MAIN TITLES ---------- */

h1 {
    color: #12304a !important;
    font-weight: 700;
}

h2, h3 {
    color: #1c4966 !important;
    font-weight: 600;
}


/* ---------- NORMAL TEXT ---------- */

p, label {
    color: #1e1e1e !important;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background-color: #12304a;
    border-right: 2px solid #0e2233;
}


/* Sidebar titles/text */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: white !important;
}


/* ---------- BUTTONS ---------- */

div.stButton > button {
    background-color: #45b6fe !important;
    color: white !important;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #3792cb !important;
    color: white !important;
}

/* ---------- DOWNLOAD BUTTON ---------- */

div.stDownloadButton > button {
    background-color: #45b6fe !important;
    color: white !important;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
}

div.stDownloadButton > button:hover {
    background-color: #3792cb !important;
    color: white !important;
}

/* ---------- INPUT BOXES ---------- */

.stNumberInput input {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}


/* ---------- SELECTBOX ---------- */

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #12304a !important;
    border-radius: 10px !important;
    color: white !important;
}


/* Selected text */

.stSelectbox span {
    color: white !important;
}


/* Dropdown menu */

div[data-baseweb="popover"] {
    background-color: #12304a !important;
    border-radius: 10px !important;
}


/* Dropdown options */

div[role="option"] {
    background-color: #12304a !important;
    color: white !important;
}


/* Hover option */

div[role="option"]:hover {
    background-color: #1c4966 !important;
    color: white !important;
}


/* ---------- CHECKBOXES ---------- */

.stCheckbox label {
    color: #1e1e1e !important;
    font-weight: 500;
}


/* ---------- CONTAINERS ---------- */

[data-testid="stContainer"] {
    border-radius: 15px;
}


/* ---------- ALERT BOXES ---------- */

.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

model = pickle.load(open("models/anemia_model.pkl", "rb"))


# =========================================================
# FUNCTIONS
# =========================================================

def check_hemoglobin(hb, gender):

    if gender == 0:

        if hb < 12:
            return "Low"

        elif hb <= 15.5:
            return "Normal"

        else:
            return "High"

    else:

        if hb < 13.5:
            return "Low"

        elif hb <= 17.5:
            return "Normal"

        else:
            return "High"


def check_rbc(rbc, gender):

    if gender == 0:

        if rbc < 4.0:
            return "Low"

        elif rbc <= 5.2:
            return "Normal"

        else:
            return "High"

    else:

        if rbc < 4.5:
            return "Low"

        elif rbc <= 5.9:
            return "Normal"

        else:
            return "High"


def check_mcv(mcv):

    if mcv < 80:
        return "Low"

    elif mcv <= 100:
        return "Normal"

    else:
        return "High"


def check_mch(mch):

    if mch < 27:
        return "Low"

    elif mch <= 33:
        return "Normal"

    else:
        return "High"


def check_mchc(mchc):

    if mchc < 32:
        return "Low"

    elif mchc <= 36:
        return "Normal"

    else:
        return "High"


def check_rdw(rdw):

    if rdw < 11.5:
        return "Low"

    elif rdw <= 14.5:
        return "Normal"

    else:
        return "High"


def anemia_severity(hb, gender):

    if gender == 0:

        if hb >= 12:
            return "No Anemia"

        elif hb >= 10:
            return "Mild Anemia"

        elif hb >= 8:
            return "Moderate Anemia"

        else:
            return "Severe Anemia"

    else:

        if hb >= 13.5:
            return "No Anemia"

        elif hb >= 11:
            return "Mild Anemia"

        elif hb >= 8:
            return "Moderate Anemia"

        else:
            return "Severe Anemia"


def possible_cause(mcv):

    if mcv < 80:
        return "Possible Iron Deficiency Anemia"

    elif mcv > 100:
        return "Possible Vitamin B12 / Folate Deficiency"

    else:
        return "Requires Further Clinical Evaluation"


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
        Paragraph(
            f"<b>AI Prediction:</b> {prediction_text}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"<b>Severity Level:</b> {severity}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"<b>Possible Cause:</b> {cause}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"<b>Diet Recommendation:</b><br/><br/>{diet.replace(chr(10), '<br/>')}",
            styles['BodyText']
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🩸 Clinical Anemia System")

mode = st.sidebar.radio(
    "Select Analysis Mode",
    ["Blood Report Analysis", "Symptom Checker"]
)


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown("""
<h1 style='text-align:center;'>
Clinical Anemia Assessment Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:gray; font-size:18px;'>
AI-Assisted Clinical Screening & Blood Report Analysis
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# =========================================================
# BLOOD REPORT MODE
# =========================================================

if mode == "Blood Report Analysis":

    st.subheader("Patient Information")

    col_a, col_b = st.columns(2)

    with col_a:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            step=1
        )

    with col_b:
        gender_option = st.selectbox(
            "Select Gender",
            ["Female", "Male"]
        )

    if gender_option == "Female":
        gender = 0
    else:
        gender = 1

    st.markdown("---")

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

    st.markdown("---")

    if st.button("Analyze Report"):

        input_data = np.array([
            [gender, hemoglobin, mch, mchc, mcv]
        ])

        prediction = model.predict(input_data)

        severity = anemia_severity(
            hemoglobin,
            gender
        )

        cause = possible_cause(mcv)

        diet = diet_recommendation(severity)

        hb_status = check_hemoglobin(
            hemoglobin,
            gender
        )

        rbc_status = check_rbc(
            rbc,
            gender
        )

        mcv_status = check_mcv(mcv)

        mch_status = check_mch(mch)

        mchc_status = check_mchc(mchc)

        rdw_status = check_rdw(rdw)

        st.subheader("Blood Parameter Analysis")

        analysis_col1, analysis_col2, analysis_col3 = st.columns(3)

        with analysis_col1:
            st.info(f"Hemoglobin: {hb_status}")
            st.info(f"RBC: {rbc_status}")

        with analysis_col2:
            st.info(f"MCV: {mcv_status}")
            st.info(f"MCH: {mch_status}")

        with analysis_col3:
            st.info(f"MCHC: {mchc_status}")
            st.info(f"RDW: {rdw_status}")

        st.markdown("---")

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

        st.markdown("---")

        st.error(
            "⚠️ This system is intended only for AI-assisted screening "
            "and educational purposes. Please consult a healthcare "
            "professional for medical diagnosis."
        )

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

    st.subheader("Symptom-Based Risk Assessment")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        step=1
    )
    
    gender_option = st.selectbox(
          "Select Gender",
          ["Female", "Male"],
          key="symptom_gender"
    )

    if gender_option == "Female":
          gender = 0
    else:
          gender = 1
          
          
          
    st.markdown("---")

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

    st.markdown("---")

    if st.button("Analyze Symptoms"):

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

        st.subheader("Clinical Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            with st.container(border=True):

                st.markdown("### Risk Assessment")

                st.warning(risk)

        with summary_col2:

            with st.container(border=True):

                st.markdown("### Severity Interpretation")

                st.info(severity)

        st.markdown("---")

        st.error(
            "⚠️ This symptom-based analysis is not a medical diagnosis. "
            "Please consult a healthcare professional and undergo proper "
            "blood testing for accurate evaluation."
        )