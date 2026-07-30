def categorize(df):

    rules = {
        "Google": "Marketing",
        "Meta": "Marketing",
        "Facebook": "Marketing",
        "OpenAI": "AI",
        "Dropbox": "Software",
        "Microsoft": "Software",
        "Vodafone": "Telefon",
        "T-Mobile": "Telefon",
        "O2": "Telefon",
        "ČEZ": "Energie",
        "PRE": "Energie",
        "Shell": "Auto",
        "OMV": "Auto",
        "MOL": "Auto",
        "FÚ": "Daně",
        "Finanční úřad": "Daně",
        "ČSSZ": "Odvody",
        "VZP": "Zdravotní pojištění",
    }

    df["Kategorie"] = "Ostatní"

    for keyword, category in rules.items():

        mask = (
            df["protistrana"].fillna("").str.contains(keyword, case=False)
            |
            df["popis transakce"].fillna("").str.contains(keyword, case=False)
        )

        df.loc[mask, "Kategorie"] = category

    return df
