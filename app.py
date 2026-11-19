import joblib
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="SMS Phishing Detector v2", layout="centered")


@st.cache_resource
def load_model():
    bundle = joblib.load("phishing_detector_v2_1.joblib")
    embedder = SentenceTransformer(bundle["embedding_model"])
    embedder.max_seq_length = 128
    return bundle["classifier"], embedder, bundle.get("threshold", 0.5)


clf, embedder, threshold = load_model()
scam_index = list(clf.classes_).index(1)

st.title("SMS Phishing & Smishing Detector (v2)")
st.write(
    "Paste an SMS or WhatsApp message to check its scam risk. "
    "Built for Nigerian-context scams such as BVN, PIN, OTP and fake-fee messages."
)

msg = st.text_area("Message text:", height=140)

if st.button("Analyze message"):
    if not msg.strip():
        st.warning("Please enter a message first.")
    else:
        emb = embedder.encode([msg])
        risk = float(clf.predict_proba(emb)[0][scam_index])

        if risk >= threshold:
            st.error(f"LIKELY SCAM / PHISHING (risk: {risk:.0%})")
        elif risk >= 0.30:
            st.warning(
                f"SUSPICIOUS (risk: {risk:.0%}). Do not click links or share anything. "
                "Verify through the official app or website."
            )
        else:
            st.success(f"Looks normal (risk: {risk:.0%})")

st.caption(
    "This is a learning project tested on small datasets, so it can be wrong. "
    "Never share your PIN, OTP, BVN or password with anyone."
)
