import streamlit as st
import pandas as pd

# Nastavení stránky
st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

# Nadpis
st.title("📊 Business Cockpit")
st.write("Nahraj bankovní výpis ve formátu CSV nebo Excel.")

# Nahrání souboru
uploaded_file = st.file_uploader(
    "Vyber soubor",
    type=["csv", "xlsx"]
)

# Zpracování souboru
if uploaded_file is not None:

    try:
        # CSV
        if uploaded_file.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(
                    uploaded_file,
                    sep=";",
                    encoding="cp1250"
                )
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";")

        # Excel
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Soubor byl úspěšně načten.")

        st.write(f"Počet řádků: **{len(df)}**")
        st.write(f"Počet sloupců: **{len(df.columns)}**")

        st.subheader("Data")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Nepodařilo se načíst soubor: {e}")
