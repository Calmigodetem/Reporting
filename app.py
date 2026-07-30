import streamlit as st

from utils.loader import load_file
from utils.metrics import calculate_metrics

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Cockpit")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    df = load_file(uploaded_file)

    metrics = calculate_metrics(df)

    st.success("✅ Soubor načten")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Stav účtu",
        f"{metrics['balance']:,.2f} Kč".replace(",", " ")
    )

    c2.metric(
        "📈 Příjmy",
        f"{metrics['income']:,.2f} Kč".replace(",", " ")
    )

    c3.metric(
        "📉 Výdaje",
        f"{metrics['expense']:,.2f} Kč".replace(",", " ")
    )

    c4.metric(
        "📊 Cashflow",
        f"{metrics['cashflow']:,.2f} Kč".replace(",", " ")
    )

    st.divider()

    st.dataframe(df, use_container_width=True)
