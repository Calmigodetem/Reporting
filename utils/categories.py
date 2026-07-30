def categorize(df):

    rules = {
        "Google": "Marketing",
        "Meta": "Marketing",
        "Facebook": "Marketing",
        "LinkedIn": "Marketing",
        "Seznam": "Marketing",
        "OpenAI": "AI",
        "Anthropic": "AI",
        "Claude": "AI",
        "Perplexity": "AI",
        "Dropbox": "Software",
        "Microsoft": "Software",
        "Adobe": "Software",
        "JetBrains": "Software",
        "Atlassian": "Software",
        "Figma": "Software",
        "Canva": "Software",
        "Notion": "Software",
        "Slack": "Software",
        "GitHub": "Software",
        "Google Cloud": "Cloud",
        "AWS": "Cloud",
        "Amazon Web Services": "Cloud",
        "Azure": "Cloud",
        "Vodafone": "Telefon",
        "T-Mobile": "Telefon",
        "O2": "Telefon",
        "ČEZ": "Energie",
        "PRE": "Energie",
        "E.ON": "Energie",
        "Innogy": "Energie",
        "Shell": "Auto",
        "OMV": "Auto",
        "MOL": "Auto",
        "Benzina": "Auto",
        "Orlen": "Auto",
        "Booking": "Cestování",
        "Airbnb": "Cestování",
        "RegioJet": "Cestování",
        "České dráhy": "Cestování",
        "Uber": "Cestování",
        "Bolt": "Cestování",
        "Lidl": "Potraviny",
        "Albert": "Potraviny",
        "Kaufland": "Potraviny",
        "Billa": "Potraviny",
        "Penny": "Potraviny",
        "Tesco": "Potraviny",
        "Makro": "Potraviny",
        "FÚ": "Daně",
        "Finanční úřad": "Daně",
        "ČSSZ": "Odvody",
        "VZP": "Zdravotní pojištění",
        "Kooperativa": "Pojištění",
        "Allianz": "Pojištění",
        "ČPP": "Pojištění",
    }

    df["Kategorie"] = "Ostatní"

    for keyword, category in rules.items():

        mask = (
            df["protistrana"]
            .fillna("")
            .str.contains(keyword, case=False)
            |
            df["popis transakce"]
            .fillna("")
            .str.contains(keyword, case=False)
        )

        df.loc[mask, "Kategorie"] = category

    return df
