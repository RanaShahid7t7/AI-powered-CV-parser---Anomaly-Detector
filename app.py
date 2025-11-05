import streamlit as st
import pdfplumber
import re
import pandas as pd
import os

EXCEL_FILE = "all_cvs_dataset.xlsx"

# ---------------- Function to process one CV ----------------
def process_cv(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # --- Extract fields ---
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    lines = text.split("\n")
    name = lines[0].strip() if lines else None

    education = re.findall(r"(B\.Sc\.|M\.Sc\.|B\.Tech|M\.Tech|Ph\.D|University|College).*", text)
    experience = re.findall(r"(?:Experience|Work History|Employment).*", text, re.IGNORECASE)
    skills = re.findall(r"(?:Skills|Technologies|Expertise).*", text, re.IGNORECASE)

    cv_data = {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "education": "; ".join(education),
        "experience": "; ".join(experience),
        "skills": "; ".join(skills),
    }

    # --- Rule-based anomaly checks ---
    anomalies = []
    if not cv_data["email"]:
        anomalies.append("Missing email")
    if not cv_data["phone"]:
        anomalies.append("Missing phone")
    if not cv_data["education"]:
        anomalies.append("Missing education")
    if not cv_data["experience"]:
        anomalies.append("Missing experience")
    if not cv_data["skills"]:
        anomalies.append("Missing skills")

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", cv_data["email"]):
        anomalies.append("Invalid email")
    if phone and len(re.sub(r"\D", "", cv_data["phone"])) < 8:
        anomalies.append("Invalid phone")

    report = cv_data | {
        "anomalies": "; ".join(anomalies),
        "valid": len(anomalies) == 0
    }
    return report

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="CV Parser & Anomaly Detector", layout="wide")

st.title("📄 CV Parser & Anomaly Detector")
st.write("Upload CV PDFs → Extract data → Detect anomalies → Save to Excel")

uploaded_files = st.file_uploader("Upload CV PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []

    for file in uploaded_files:
        report = process_cv(file)
        report["file"] = file.name  # Add filename
        results.append(report)

    df = pd.DataFrame(results)

    # Show results in Streamlit
    st.subheader("📊 Extracted CV Data")
    st.dataframe(df, use_container_width=True)

    # --- Save or append to Excel ---
    if os.path.exists(EXCEL_FILE):
        old_df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        df = pd.concat([old_df, df], ignore_index=True)

    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

    st.success(f"✅ Data saved to {EXCEL_FILE}")

    # --- Download button ---
    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label="⬇️ Download Updated Excel",
            data=f,
            file_name=EXCEL_FILE,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
