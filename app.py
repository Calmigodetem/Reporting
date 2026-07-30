import streamlit as st

from utils.loader import load_file
from utils.metrics import calculate_metrics
from utils.charts import balance_chart, category_chart
from utils.filters import filter_data
from utils.categories import categorize

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)


def czk(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ") + " Kč"


st.title("📊 Business Cockpit")
st.sidebar.title("Filtry")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis",
    type=["csv", "xlsx"]
)

if uploaded_file:

    df = load_file(uploaded_file)
    df = categorize(df)
    df = filter_data(df)

    metrics = calculate_metrics(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Stav účtu", czk(metrics["balance"]))
    c2.metric("📈 Příjmy", czk(metrics["income"]))
    c3.metric("📉 Výdaje", czk(metrics["expense"]))
    c4.metric("📊 Cashflow", czk(metrics["cashflow"]))

    st.plotly_chart(
        balance_chart(df),
        use_container_width=True
    )

    st.plotly_chart(
        category_chart(df),
        use_container_width=True
    )

    st.dataframe(
        df[
            [
                "datum zaúčtování",
                "Kategorie",
                "částka platby",
                "protistrana",
                "popis transakce",
            ]
        ].sort_values(
            "datum zaúčtování",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )
