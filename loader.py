import pandas as pd


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

    df["částka platby"] = (
        df["částka platby"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["zůstatek"] = (
        df["zůstatek"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    return df
