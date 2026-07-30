import streamlit as st

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Cockpit")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis (CSV nebo Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    st.success("Soubor byl úspěšně nahrán.")
