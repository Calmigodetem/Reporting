import streamlit as st

from utils.loader import load_file
from utils.metrics import calculate_metrics
from utils.charts import balance_chart

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)


def czk(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ") + " Kč"


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

    c1.metric("💰 Stav účtu", czk(metrics["balance"]))
    c2.metric("📈 Příjmy", czk(metrics["income"]))
    c3.metric("📉 Výdaje", czk(metrics["expense"]))
    c4.metric("📊 Cashflow", czk(metrics["cashflow"]))

    st.divider()

    st.plotly_chart(
        balance_chart(df),
        use_container_width=True
    )

    st.divider()

    st.subheader("Posledních 20 transakcí")

    columns = [
        "datum zaúčtování",
        "částka platby",
        "zůstatek",
        "protistrana",
        "popis transakce"
    ]

    st.dataframe(
        df[columns]
        .sort_values("datum zaúčtování", ascending=False)
        .head(20),
        use_container_width=True,
        hide_index=True
    )
