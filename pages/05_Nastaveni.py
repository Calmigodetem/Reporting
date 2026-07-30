import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Nastavení",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Nastavení")

CONFIG_DIR = Path("data")
CONFIG_DIR.mkdir(exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT = {
    "company_name": "",
    "currency": "CZK",
    "vat_rate": 21,
    "budget_month": 0,
    "alert_limit": 10000,
    "theme": "Světlý",
}


def load_settings():

    if CONFIG_FILE.exists():

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return DEFAULT.copy()


def save_settings(settings):

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            settings,
            f,
            ensure_ascii=False,
            indent=4,
        )


settings = load_settings()

st.subheader("Obecné")

company_name = st.text_input(
    "Název společnosti",
    settings["company_name"],
)

currency = st.selectbox(
    "Měna",
    ["CZK", "EUR", "USD"],
    index=["CZK", "EUR", "USD"].index(settings["currency"]),
)

vat_rate = st.number_input(
    "DPH (%)",
    min_value=0,
    max_value=100,
    value=int(settings["vat_rate"]),
)

st.divider()

st.subheader("Rozpočet")

budget_month = st.number_input(
    "Měsíční rozpočet",
    min_value=0,
    value=int(settings["budget_month"]),
    step=1000,
)

alert_limit = st.number_input(
    "Upozornit při transakci vyšší než",
    min_value=0,
    value=int(settings["alert_limit"]),
    step=1000,
)

st.divider()

st.subheader("Vzhled")

theme = st.radio(
    "Motiv",
    [
        "Světlý",
        "Tmavý",
    ],
    index=0 if settings["theme"] == "Světlý" else 1,
)

st.divider()

if st.button(
    "💾 Uložit nastavení",
    use_container_width=True,
):

    settings = {
        "company_name": company_name,
        "currency": currency,
        "vat_rate": vat_rate,
        "budget_month": budget_month,
        "alert_limit": alert_limit,
        "theme": theme,
    }

    save_settings(settings)

    st.success("Nastavení bylo uloženo.")

st.divider()

st.subheader("Aktuální konfigurace")

st.json(load_settings())
