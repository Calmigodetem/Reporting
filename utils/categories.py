import re


RULES = {
    "Marketing": [
        "google",
        "ads",
        "adwords",
        "meta",
        "facebook",
        "instagram",
        "linkedin",
        "seznam",
    ],
    "Software": [
        "microsoft",
        "adobe",
        "jetbrains",
        "github",
        "gitlab",
        "notion",
        "atlassian",
        "figma",
        "slack",
        "zoom",
        "dropbox",
        "canva",
    ],
    "AI": [
        "openai",
        "chatgpt",
        "anthropic",
        "claude",
        "perplexity",
        "gemini",
    ],
    "Cloud": [
        "aws",
        "amazon web services",
        "azure",
        "google cloud",
        "digitalocean",
        "ovh",
    ],
    "Energie": [
        "čez",
        "cez",
        "eon",
        "e.on",
        "pre",
        "innogy",
    ],
    "Telefon": [
        "vodafone",
        "t-mobile",
        "tmobile",
        "o2",
    ],
    "Potraviny": [
        "lidl",
        "albert",
        "tesco",
        "kaufland",
        "billa",
        "penny",
        "globus",
        "makro",
    ],
    "Auto": [
        "shell",
        "omv",
        "orlen",
        "benzina",
        "mol",
    ],
    "Cestování": [
        "booking",
        "airbnb",
        "ryanair",
        "wizz",
        "uber",
        "bolt",
        "regiojet",
        "české dráhy",
    ],
    "Daně": [
        "finanční úřad",
        "financni urad",
        "fú",
    ],
    "Pojištění": [
        "kooperativa",
        "allianz",
        "čpp",
        "cpp",
        "generali",
    ],
    "Zdravotní pojištění": [
        "vzp",
        "ozp",
    ],
    "Odvody": [
        "čssz",
        "cssz",
    ],
}


def normalize(text):

    if text is None:
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text


def categorize(df):

    df["Kategorie"] = "Ostatní"

    for index, row in df.iterrows():

        text = normalize(
            str(row.get("protistrana", ""))
            + " "
            + str(row.get("popis transakce", ""))
        )

        assigned = False

        for category, keywords in RULES.items():

            if assigned:
                break

            for keyword in keywords:

                if keyword in text:

                    df.at[index, "Kategorie"] = category
                    assigned = True
                    break

    return df
