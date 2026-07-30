import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Zákazníci",
    page_icon="👥",
    layout="wide",
)


st.title("👥 Analýza zákazníků")


if "df" not in st.session_state:
    st.warning(
        "Nejprve nahraj data na hlavní stránce."
    )
    st.stop()


df = st.session_state["df"].copy()


# pouze příjmy
customers = df[
    df["částka platby"] > 0
].copy()


if customers.empty:

    st.info(
        "Nenalezeny žádné příchozí platby."
    )

    st.stop()


# odstranění prázdných názvů

customers["protistrana"] = (
    customers["protistrana"]
    .fillna("Neznámý zákazník")
)


customers.loc[
    customers["protistrana"].str.strip() == "",
    "protistrana"
] = "Neznámý zákazník"



# KPI

total_income = customers["částka platby"].sum()

count_customers = (
    customers["protistrana"]
    .nunique()
)


avg_payment = (
    customers["částka platby"]
    .mean()
)


c1,c2,c3 = st.columns(3)


c1.metric(
    "Tržby",
    f"{total_income:,.0f} Kč"
)

c2.metric(
    "Počet zákazníků",
    count_customers
)

c3.metric(
    "Průměrná platba",
    f"{avg_payment:,.0f} Kč"
)



st.divider()


# TOP zákazníci

summary = (
    customers
    .groupby("protistrana")
    .agg(
        Obrat=(
            "částka platby",
            "sum"
        ),
        Transakce=(
            "částka platby",
            "count"
        ),
        Průměrná_platba=(
            "částka platby",
            "mean"
        ),
        Poslední_platba=(
            "datum zaúčtování",
            "max"
        )
    )
    .reset_index()
)


summary = summary.sort_values(
    "Obrat",
    ascending=False
)



left,right = st.columns(2)


with left:

    fig = px.bar(
        summary.head(10),
        x="Obrat",
        y="protistrana",
        orientation="h",
        title="TOP 10 zákazníků podle obratu",
        text_auto=".2s",
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with right:

    fig = px.pie(
        summary.head(10),
        names="protistrana",
        values="Obrat",
        hole=0.45,
        title="Podíl TOP zákazníků",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



st.divider()


# vývoj zákazníků

customers["Měsíc"] = (
    customers["datum zaúčtování"]
    .dt.to_period("M")
    .astype(str)
)


trend = (
    customers
    .groupby(
        [
            "Měsíc",
            "protistrana"
        ]
    )["částka platby"]
    .sum()
    .reset_index()
)



fig = px.line(
    trend[
        trend["protistrana"]
        .isin(summary.head(5)["protistrana"])
    ],
    x="Měsíc",
    y="částka platby",
    color="protistrana",
    markers=True,
    title="Vývoj TOP zákazníků",
)


st.plotly_chart(
    fig,
    use_container_width=True
)



st.divider()


st.subheader(
    "📋 Detail zákazníků"
)


st.dataframe(
    summary.style.format(
        {
            "Obrat": "{:,.0f} Kč",
            "Průměrná_platba": "{:,.0f} Kč",
        }
    ),
    use_container_width=True,
    hide_index=True,
)
