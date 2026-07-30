import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_file(uploaded_file):

    if uploaded_file.name.lower().endswith(".csv"):

        for encoding in [
            "cp1250",
            "utf-8",
            "utf-8-sig",
            "latin1",
        ]:

            try:
                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    sep=";",
                    encoding=encoding,
                )

                break

            except Exception:
                continue

    else:

        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    rename = {
        "datum": "datum zaúčtování",
        "datum zauctovani": "datum zaúčtování",
        "datum zaúčtování": "datum zaúčtování",
        "datum zaúčtovani": "datum zaúčtování",

        "částka": "částka platby",
        "castka": "částka platby",
        "částka platby": "částka platby",
        "castka platby": "částka platby",

        "zůstatek": "zůstatek",
        "zustatek": "zůstatek",

        "partner": "protistrana",
        "protistrana": "protistrana",
        "protistrana / příjemce": "protistrana",
        "protistrana/prijemce": "protistrana",
        "název protiúčtu": "protistrana",
        "nazev protiuctu": "protistrana",

        "poznámka": "popis transakce",
        "poznamka": "popis transakce",
        "popis": "popis transakce",
        "popis transakce": "popis transakce",
    }

    df.rename(columns=rename, inplace=True)

    required = [
        "datum zaúčtování",
        "částka platby",
        "protistrana",
        "popis transakce",
    ]

    for column in required:

        if column not in df.columns:
            df[column] = ""

    if "zůstatek" not in df.columns:
        df["zůstatek"] = 0

    df["datum zaúčtování"] = pd.to_datetime(
        df["datum zaúčtování"],
        dayfirst=True,
        errors="coerce",
    )

    for column in [
        "částka platby",
        "zůstatek",
    ]:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace(" ", "", regex=False)
            .str.replace("\xa0", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.replace("CZK", "", regex=False)
            .str.replace("Kč", "", regex=False)
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        ).fillna(0)

    df = df.sort_values(
        "datum zaúčtování"
    ).reset_index(drop=True)

    return df
