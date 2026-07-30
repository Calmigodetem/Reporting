import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Business Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Dashboard")

uploaded_file = st.file_uploader(
    "Nahraj CSV nebo Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):

        try:
            df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=";", encoding="cp1250")

    else:

        df = pd.read_excel(uploaded_file)

    st.success(f"Načteno {len(df)} řádků")

    st.dataframe(df)

    st.write("### Sloupce")

    st.write(df.columns.tolist())
