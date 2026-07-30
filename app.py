import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Nastavení stránky
# -----------------------------
st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Cockpit")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis (CSV nebo Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Načtení souboru
        if uploaded_file.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, sep=";", encoding="cp1250")
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";")
        else:
            df = pd.read_excel(uploaded_file)

        # -----------------------------
        # Převod dat
        # -----------------------------

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

        # -----------------------------
        # KPI
        # -----------------------------

        aktualni_zustatek = df["zůstatek"].iloc[-1]
        prijmy = df[df["částka platby"] > 0]["částka platby"].sum()
        vydaje = abs(df[df["částka platby"] < 0]["částka platby"].sum())
        cashflow = prijmy - vydaje

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "💰 Stav účtu",
            f"{aktualni_zustatek:,.2f} Kč".replace(",", " ")
        )

        c2.metric(
            "📈 Příjmy",
            f"{prijmy:,.2f} Kč".replace(",", " ")
        )

        c3.metric(
            "📉 Výdaje",
            f"{vydaje:,.2f} Kč".replace(",", " ")
        )

        c4.metric(
            "📊 Cashflow",
            f"{cashflow:,.2f} Kč".replace(",", " ")
        )

        # -----------------------------
        # Graf
        # -----------------------------

        fig = px.line(
            df,
            x="datum zaúčtování",
            y="zůstatek",
            title="Vývoj zůstatku"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # Tabulka
        # -----------------------------

        st.subheader("Posledních 20 transakcí")

        st.dataframe(
            df.sort_values("datum zaúčtování", ascending=False)
            .head(20),
            use_container_width=True
        )

    except Exception as e:
        st.error(e)
