import streamlit as st
import pandas as pd
from utils.metrics import calculate_metrics
from utils.charts import (
    balance_chart,
    monthly_chart,
    category_chart,
    cashflow_chart,
)

st.set_page_config(
    page_title="Přehled",
    layout="wide",
)

st.title("📈 Přehled")

if "df" not in st.session_state:

    st.warning("Nejprve nahraj data na hlavní stránce.")
    st.stop()

df = st.session_state["df"]

metrics = calculate_metrics(df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Příjmy", f"{metrics['income']:,.0f} Kč")
c2.metric("Výdaje", f"{metrics['expense']:,.0f} Kč")
c3.metric("Cashflow", f"{metrics['cashflow']:,.0f} Kč")
c4.metric("Účet", f"{metrics['balance']:,.0f} Kč")

l, r = st.columns(2)

with l:

    st.plotly_chart(
        balance_chart(df),
        use_container_width=True,
    )

    st.plotly_chart(
        monthly_chart(df),
        use_container_width=True,
    )

with r:

    st.plotly_chart(
        category_chart(df),
        use_container_width=True,
    )

    st.plotly_chart(
        cashflow_chart(df),
        use_container_width=True,
    )

st.subheader("Poslední transakce")

st.dataframe(
    df.sort_values(
        "datum zaúčtování",
        ascending=False,
    ).head(20),
    use_container_width=True,
    hide_index=True,
)
