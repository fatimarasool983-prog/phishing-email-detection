# ==========================================
# SECTION 1: IMPORT REQUIRED LIBRARIES
# ==========================================
import streamlit as st
import pandas as pd
import joblib
import re
import os
# ==========================================
# SECTION 2: LOAD TRAINED MODEL AND VECTORIZER
# ==========================================
model = joblib.load("phishing_model_bigrams.pkl")

tfidf = joblib.load("tfidf_vectorizer_bigrams.pkl")
# ==========================================
# SECTION 3: EMAIL TEXT CLEANING
# ==========================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
# ==========================================
# SECTION 4: STREAMLIT PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Phishing Email Detection",
    page_icon="📧",
    layout="centered"
)
# ==========================================
# SECTION 5: APPLICATION TITLE AND DESCRIPTION
# ==========================================
st.title("📧 Phishing Email Detection System")
st.write(
    "This application uses Machine Learning "
    "to detect whether an email is Phishing or Legitimate."
)
# ==========================================
# SECTION 6: EMAIL INPUT AREA
# ==========================================
st.subheader("Enter Email for Analysis")
email_input = st.text_area(
    "Paste your email text here:",
    height=200,
    placeholder="Enter or paste your email..."
)
# ==========================================
# SECTION 7: PREDICTION BUTTON
# ==========================================
predict_button = st.button("Analyze Email")

# ==========================================
# SECTION 8: EMAIL PREDICTION LOGIC
# ==========================================

if predict_button:

    if email_input.strip():

        email_tfidf = tfidf.transform([email_input])

        prediction = model.predict(email_tfidf)[0]

        probabilities = model.predict_proba(email_tfidf)[0]

        confidence = max(probabilities) * 100

        if prediction == 1:
            st.error("⚠️ This is a Phishing Email!")

        else:
            st.success("✅ This is a Legitimate Email!")

        st.info(f"Prediction Confidence: {confidence:.2f}%")

    else:
        st.warning("Please enter an email before analyzing.")

 # ==========================================
# SECTION 9: APPLICATION FOOTER
# ==========================================
st.markdown("---")
# Security Disclaimer
st.info(
    "Security Notice: This tool provides predictions "
    "based on email text only. Results may be incorrect. "
    "Always verify suspicious emails through official sources. "
    "Never share passwords or OTPs."
)
st.caption(
    "Phishing Email Detection System | "
    "Developed using Python, Streamlit and Machine Learning"
)
