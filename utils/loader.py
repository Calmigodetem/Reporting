import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = [
    "datum zaúčtování",
    "částka platby",
]


def _normalize_columns(df):

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    rename = {
        "datum": "datum zaúčtování",
        "datum zauctovani": "datum zaúčtování",
        "datum zaúčtování": "datum zaúčtování",
        "date": "datum zaúčtování",
        "částka": "částka platby",
        "castka": "částka platby",
        "částka platby": "částka platby",
        "amount": "částka platby",
        "balance": "zůstatek",
        "zůstatek": "zůstatek",
        "popis": "popis transakce",
        "poznámka": "popis transakce",
        "detail": "popis transakce",
        "protistrana": "protistrana",
        "partner": "protistrana",
        "název protiúčtu": "protistrana",
    }

    df = df.rename(columns=rename)

    return df


def load_file(uploaded_file):

    name = uploaded_file.name.lower()

    if name.endswith(".csv"):

        separators = [
            ";",
            ",",
            "\t",
        ]

        df = None

        for sep in separators:
            try:
                uploaded_file.seek(0)
                tmp = pd.read_csv(
                    uploaded_file,
                    sep=sep,
                    encoding="utf-8",
                )

                if len(tmp.columns) > 1:
                    df = tmp
                    break

            except Exception:
                pass

        if df is None:
            uploaded_file.seek(0)
            df = pd.read_csv(
                uploaded_file,
                sep=";",
                encoding="cp1250",
            )

    elif name.endswith(".xlsx"):

        df = pd.read_excel(uploaded_file)

    else:

        st.error("Nepodporovaný formát.")
        st.stop()

    df = _normalize_columns(df)

    missing = [
        c for c in REQUIRED_COLUMNS
        if c not in df.columns
    ]

    if missing:

        st.error(
            "Chybí povinné sloupce:\n\n"
            + "\n".join(missing)
        )
        st.stop()

    df["datum zaúčtování"] = pd.to_datetime(
        df["datum zaúčtování"],
        errors="coerce",
        dayfirst=True,
    )

    df["částka platby"] = (
        df["částka platby"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["částka platby"] = pd.to_numeric(
        df["částka platby"],
        errors="coerce",
    )

    if "zůstatek" in df.columns:

        df["zůstatek"] = (
            df["zůstatek"]
            .astype(str)
            .str.replace(" ", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df["zůstatek"] = pd.to_numeric(
            df["zůstatek"],
            errors="coerce",
        )

    else:

        df["zůstatek"] = (
            df["částka platby"]
            .cumsum()
        )

    if "protistrana" not in df.columns:
        df["protistrana"] = ""

    if "popis transakce" not in df.columns:
        df["popis transakce"] = ""

    df = df.dropna(
        subset=[
            "datum zaúčtování",
            "částka platby",
        ]
    )

    df = df.sort_values(
        "datum zaúčtování"
    ).reset_index(drop=True)

    return df
