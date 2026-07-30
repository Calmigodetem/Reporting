import pandas as pd
import streamlit as st


def normalize_columns(df):

    # odstranění duplicitních názvů
    df = df.loc[:, ~df.columns.duplicated()]

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    rename = {

        # datum
        "datum": "datum zaúčtování",
        "date": "datum zaúčtování",
        "datum zaúčtovani": "datum zaúčtování",
        "datum zaúčtování": "datum zaúčtování",

        # částka
        "částka": "částka platby",
        "castka": "částka platby",
        "amount": "částka platby",
        "částka platby": "částka platby",

        # zůstatek
        "zustatek": "zůstatek",
        "zůstatek": "zůstatek",
        "balance": "zůstatek",

        # popis
        "popis": "popis transakce",
        "detail": "popis transakce",
        "poznámka": "popis transakce",
        "text": "popis transakce",

        # protistrana
        "partner": "protistrana",
        "protiucet": "protistrana",
        "protistrana": "protistrana",
        "název protiúčtu": "protistrana",
    }

    df = df.rename(
        columns=rename
    )

    # znovu kontrola po rename
    df = df.loc[:, ~df.columns.duplicated()]

    return df


def read_file(uploaded_file):

    name = uploaded_file.name.lower()

    if name.endswith(".csv"):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1250",
            "latin1",
        ]

        separators = [
            ";",
            ",",
            "\t",
        ]

        for enc in encodings:

            for sep in separators:

                try:

                    uploaded_file.seek(0)

                    df = pd.read_csv(
                        uploaded_file,
                        sep=sep,
                        encoding=enc,
                    )

                    if len(df.columns) > 1:
                        return df

                except Exception:
                    pass


        raise ValueError(
            "CSV soubor nelze načíst."
        )


    elif name.endswith(".xlsx"):

        return pd.read_excel(
            uploaded_file
        )


    else:

        raise ValueError(
            "Nepodporovaný formát."
        )


def clean_amount(value):

    if pd.isna(value):
        return 0

    value = str(value)

    value = (
        value
        .replace(" ", "")
        .replace("\xa0", "")
        .replace(",", ".")
    )

    value = (
        value
        .replace("Kč", "")
        .replace("CZK", "")
    )

    try:
        return float(value)

    except:
        return 0


def load_file(uploaded_file):

    try:

        df = read_file(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"Chyba načtení souboru: {e}"
        )

        st.stop()


    df = normalize_columns(df)


    required = [
        "datum zaúčtování",
        "částka platby",
    ]


    missing = [
        c
        for c in required
        if c not in df.columns
    ]


    if missing:

        st.error(
            "Chybí sloupce: "
            + ", ".join(missing)
        )

        st.write(
            "Dostupné sloupce:",
            list(df.columns)
        )

        st.stop()



    df["datum zaúčtování"] = pd.to_datetime(
        df["datum zaúčtování"],
        errors="coerce",
        dayfirst=True,
    )


    df["částka platby"] = (
        df["částka platby"]
        .apply(clean_amount)
    )


    if "zůstatek" in df.columns:

        df["zůstatek"] = (
            df["zůstatek"]
            .apply(clean_amount)
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
            "datum zaúčtování"
        ]
    )


    df = df.sort_values(
        "datum zaúčtování"
    )


    df = df.reset_index(
        drop=True
    )


    # poslední ochrana proti duplicitám
    df = df.loc[
        :,
        ~df.columns.duplicated()
    ]


    return df
