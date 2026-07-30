import re
import pandas as pd


RULES = {
    "Potraviny": [
        "lidl", "kaufland", "albert", "tesco",
        "billa", "globus", "penny",
    ],

    "Restaurace": [
        "restaurant", "rest", "pizza",
        "bistro", "kebab", "burger",
        "mcdonald", "kfc",
    ],

    "Palivo": [
        "shell", "omv", "mol",
        "benzina", "orlen",
    ],

    "Doprava": [
        "uber", "bolt", "regiojet",
        "ceske drahy", "čd",
    ],

    "Energie": [
        "cez", "čez", "pre",
        "innogy",
    ],

    "Telefon": [
        "o2",
        "vodafone",
        "t-mobile",
    ],

    "Software": [
        "microsoft",
        "google",
        "apple",
        "openai",
        "github",
    ],

    "Pojištění": [
        "allianz",
        "kooperativa",
        "generali",
    ],

    "Nákupy": [
        "alza",
        "datart",
        "ikea",
        "hornbach",
    ],

    "Ostatní služby": [
        "service",
        "cloud",
        "hosting",
    ],
}


def _clean(text):

    if text is None:
        return ""

    if isinstance(text, (list, tuple)):
        text = " ".join(
            str(x)
            for x in text
        )

    if pd.isna(text) is True:
        return ""

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def categorize(df):

    df = df.copy()

    categories = []

    for _, row in df.iterrows():

        text = (
            _clean(
                row.get(
                    "protistrana",
                    ""
                )
            )
            + " "
            +
            _clean(
                row.get(
                    "popis transakce",
                    ""
                )
            )
        )

        category = "Ostatní"

        for name, keywords in RULES.items():

            for keyword in keywords:

                if keyword in text:

                    category = name
                    break

            if category != "Ostatní":
                break

        try:

            if (
                row["částka platby"] > 0
                and category == "Ostatní"
            ):
                category = "Příjem"

        except Exception:
            pass


        categories.append(category)


    df["Kategorie"] = categories

    return df
