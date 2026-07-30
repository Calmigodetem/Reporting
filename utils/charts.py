import pandas as pd
import plotly.express as px


def balance_chart(df):

    fig = px.line(
        df.sort_values("datum zaúčtování"),
        x="datum zaúčtování",
        y="zůstatek",
        title="Vývoj zůstatku",
        markers=True,
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def category_chart(df):

    expenses = df[df["částka platby"] < 0]

    summary = (
        expenses.groupby("Kategorie")["částka platby"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.pie(
        summary,
        names="Kategorie",
        values="částka platby",
        title="Výdaje podle kategorií",
        hole=0.45,
    )

    fig.update_traces(textposition="inside")

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def monthly_chart(df):

    tmp = df.copy()

    tmp["Měsíc"] = (
        tmp["datum zaúčtování"]
        .dt.to_period("M")
        .astype(str)
    )

    income = (
        tmp[tmp["částka platby"] > 0]
        .groupby("Měsíc")["částka platby"]
        .sum()
    )

    expense = (
        tmp[tmp["částka platby"] < 0]
        .groupby("Měsíc")["částka platby"]
        .sum()
        .abs()
    )

    monthly = pd.concat(
        [income, expense],
        axis=1
    ).fillna(0)

    monthly.columns = [
        "Příjmy",
        "Výdaje",
    ]

    monthly = monthly.reset_index()

    fig = px.bar(
        monthly,
        x="Měsíc",
        y=["Příjmy", "Výdaje"],
        barmode="group",
        title="Příjmy × Výdaje po měsících",
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def top_suppliers_chart(df):

    expenses = df[df["částka platby"] < 0].copy()

    top = (
        expenses.groupby("protistrana")["částka platby"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top,
        x="částka platby",
        y="protistrana",
        orientation="h",
        title="TOP 10 příjemců plateb",
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis=dict(categoryorder="total ascending"),
    )

    return fig
