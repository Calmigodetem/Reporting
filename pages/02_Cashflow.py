import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cashflow",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Cashflow")

if "df" not in st.session_state:
    st.warning("Nejprve nahraj data na hlavní stránce.")
    st.stop()

df = st.session_state["df"].copy()

df["Měsíc"] = (
    df["datum zaúčtování"]
    .dt.to_period("M")
    .astype(str)
)

income = (
    df[df["částka platby"] > 0]
    .groupby("Měsíc")["částka platby"]
    .sum()
)

expense = (
    df[df["částka platby"] < 0]
    .groupby("Měsíc")["částka platby"]
    .sum()
    .abs()
)

cashflow = pd.concat(
    [income, expense],
    axis=1,
).fillna(0)

cashflow.columns = [
    "Příjmy",
    "Výdaje",
]

cashflow["Cashflow"] = (
    cashflow["Příjmy"] - cashflow["Výdaje"]
)

cashflow = cashflow.reset_index()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Celkové příjmy",
    f"{cashflow['Příjmy'].sum():,.0f} Kč",
)

c2.metric(
    "Celkové výdaje",
    f"{cashflow['Výdaje'].sum():,.0f} Kč",
)

c3.metric(
    "Celkové cashflow",
    f"{cashflow['Cashflow'].sum():,.0f} Kč",
)

fig = px.bar(
    cashflow,
    x="Měsíc",
    y=[
        "Příjmy",
        "Výdaje",
    ],
    barmode="group",
    text_auto=".2s",
    title="Příjmy vs Výdaje",
)

fig.update_layout(
    template="plotly_white",
    height=450,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

fig2 = px.line(
    cashflow,
    x="Měsíc",
    y="Cashflow",
    markers=True,
    title="Vývoj cashflow",
)

fig2.update_layout(
    template="plotly_white",
    height=450,
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.subheader("Měsíční přehled")

st.dataframe(
    cashflow.style.format({
        "Příjmy": "{:,.0f} Kč",
        "Výdaje": "{:,.0f} Kč",
        "Cashflow": "{:,.0f} Kč",
    }),
    use_container_width=True,
    hide_index=True,
)
