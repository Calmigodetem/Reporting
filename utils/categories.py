import re
import pandas as pd


RULES = {
    "Mzda": [
        "mzda",
        "salary",
        "výplata",
        "payroll",
    ],
    "Nájem": [
        "nájem",
        "rent",
        "pronájem",
    ],
    "Potraviny": [
        "lidl",
        "kaufland",
        "albert",
        "tesco",
        "billa",
        "globus",
        "penny",
        "coop",
    ],
    "Restaurace": [
        "restaurant",
        "rest",
        "pizza",
        "bistro",
        "kebab",
        "mcdonald",
        "burger",
        "kfc",
        "subway",
        "costa",
        "starbucks",
    ],
    "Palivo": [
        "shell",
        "omv",
        "mol",
        "benzina",
        "cepro",
        "orlen",
    ],
    "Doprava": [
        "uber",
        "bolt",
        "liftago",
        "čd",
        "regiojet",
        "dp",
    ],
    "Energie": [
        "čez",
        "pre",
        "innogy",
        "epet",
        "energie",
    ],
    "Telefon a internet": [
        "o2",
        "t-mobile",
        "vodafone",
    ],
    "Pojištění": [
        "allianz",
        "kooperativa",
        "generali",
        "čpp",
        "uniqa",
    ],
    "Daně": [
        "finanční úřad",
        "financni urad",
        "fú",
    ],
    "Bankovní poplatky": [
        "poplatek",
        "fee",
        "úrok",
        "interest",
    ],
    "Zábava": [
        "cinema",
        "kino",
        "netflix",
        "spotify",
        "hbo",
        "disney",
        "steam",
        "xbox",
        "playstation",
    ],
    "Nákupy": [
        "alza",
        "mall",
        "datart",
        "planeo",
        "ikea",
        "hornbach",
        "obi",
        "bauhaus",
    ],
    "Zdraví": [
        "lékárna",
        "dr max",
        "benu",
        "doctor",
        "hospital",
    ],
}


def _clean(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text


def categorize(df):

    df = df.copy()

    categories = []

    for _, row in df.iterrows():

        text = (
            _clean(row.get("protistrana", ""))
            + " "
            + _clean(row.get("popis transakce", ""))
        )

        category = "Ostatní"

        for name, words in RULES.items():

            if any(word in text for word in words):
                category = name
                break

        amount = row["částka platby"]

        if amount > 0 and category == "Ostatní":
            category = "Příjem"

        categories.append(category)

    df["Kategorie"] = categories

    return df
