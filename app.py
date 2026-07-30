import streamlit as st
from utils.loader import load_file

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Cockpit")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    df = load_file(uploaded_file)

    st.success("✅ Soubor načten")

    st.dataframe(df, use_container_width=True)
