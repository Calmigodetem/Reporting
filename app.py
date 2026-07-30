import streamlit as st

from utils.loader import load_file
from utils.metrics import calculate_metrics
from utils.charts import (
    balance_chart,
    category_chart,
    monthly_chart,
    top_suppliers_chart,
)
from utils.filters import filter_data
from utils.categories import categorize

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)


def czk(value):
    return (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", " ")
        + " Kč"
    )


st.title("📊 Business Cockpit")
st.sidebar.title("Filtry")

uploaded_file = st.file_uploader(
    "Nahraj bankovní výpis",
    type=["csv", "xlsx"],
)

if uploaded_file:

    df = load_file(uploaded_file)
    df = categorize(df)
    df = filter_data(df)

    metrics = calculate_metrics(df)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "💰 Stav účtu",
        czk(metrics["balance"]),
    )

    kpi2.metric(
        "📈 Příjmy",
        czk(metrics["income"]),
    )

    kpi3.metric(
        "📉 Výdaje",
        czk(metrics["expense"]),
    )

    kpi4.metric(
        "📊 Cashflow",
        czk(metrics["cashflow"]),
    )

    kpi5, kpi6, kpi7 = st.columns(3)

    kpi5.metric(
        "📄 Transakcí",
        metrics["transactions"],
    )

    kpi6.metric(
        "⬆️ Průměrný příjem",
        czk(metrics["avg_income"]),
    )

    kpi7.metric(
        "⬇️ Průměrný výdaj",
        czk(metrics["avg_expense"]),
    )

    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            balance_chart(df),
            use_container_width=True,
        )

        st.plotly_chart(
            monthly_chart(df),
            use_container_width=True,
        )

    with right:
        st.plotly_chart(
            category_chart(df),
            use_container_width=True,
        )

        st.plotly_chart(
            top_suppliers_chart(df),
            use_container_width=True,
        )

    st.subheader("Transakce")

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
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )
