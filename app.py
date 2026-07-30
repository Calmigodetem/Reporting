import streamlit as st
import pandas as pd

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

if uploaded_file is not None:

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, sep=";", encoding="cp1250")
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";")
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Soubor byl úspěšně načten.")

        st.subheader("Názvy sloupců")
        st.code("\n".join(df.columns.astype(str)))

        st.subheader("Prvních 5 řádků")
        st.dataframe(df.head(), use_container_width=True)

    except Exception as e:
        st.error(f"Chyba při načítání: {e}")
