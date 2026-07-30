import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_file(uploaded_file):

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
    else:
        df = pd.read_excel(uploaded_file)

    df["datum zaúčtování"] = pd.to_datetime(
        df["datum zaúčtování"],
        dayfirst=True,
        errors="coerce"
    )

    for column in ["částka platby", "zůstatek"]:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace(" ", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    return df
