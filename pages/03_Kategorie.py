import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Kategorie",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Analýza kategorií")

if "df" not in st.session_state:
    st.warning("Nejprve nahraj data na hlavní stránce.")
    st.stop()

df = st.session_state["df"].copy()

expenses = df[df["částka platby"] < 0].copy()

if expenses.empty:
    st.info("Nejsou k dispozici žádné výdajové transakce.")
    st.stop()

summary = (
    expenses.groupby("Kategorie")
    .agg(
        Výdaje=("částka platby", lambda x: abs(x.sum())),
        Transakcí=("částka platby", "count"),
        Průměr=("částka platby", lambda x: abs(x.mean())),
        Maximum=("částka platby", lambda x: abs(x.min())),
    )
    .reset_index()
)

summary = summary.sort_values(
    "Výdaje",
    ascending=False,
)

c1, c2 = st.columns(2)

with c1:

    fig = px.bar(
        summary,
        x="Kategorie",
        y="Výdaje",
        text_auto=".2s",
        title="Výdaje podle kategorií",
    )

    fig.update_layout(
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with c2:

    fig2 = px.pie(
        summary,
        names="Kategorie",
        values="Výdaje",
        hole=0.45,
        title="Podíl kategorií",
    )

    fig2.update_layout(
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

expenses["Měsíc"] = (
    expenses["datum zaúčtování"]
    .dt.to_period("M")
    .astype(str)
)

trend = (
    expenses.groupby(
        [
            "Měsíc",
            "Kategorie",
        ]
    )["částka platby"]
    .sum()
    .abs()
    .reset_index()
)

fig3 = px.line(
    trend,
    x="Měsíc",
    y="částka platby",
    color="Kategorie",
    markers=True,
    title="Vývoj kategorií v čase",
)

fig3.update_layout(
    template="plotly_white",
    height=500,
)

st.plotly_chart(
    fig3,
    use_container_width=True,
)

st.subheader("Souhrnná tabulka")

st.dataframe(
    summary.style.format({
        "Výdaje": "{:,.0f} Kč",
        "Průměr": "{:,.0f} Kč",
        "Maximum": "{:,.0f} Kč",
    }),
    use_container_width=True,
    hide_index=True,
)
