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

    fig.update_layout(height=420)

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
        hole=0.45,
        title="Výdaje podle kategorií",
    )

    fig.update_layout(height=420)

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
        axis=1,
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
        text_auto=".2s",
        title="Příjmy × Výdaje",
    )

    fig.update_layout(height=420)

    return fig


def top_suppliers_chart(df):

    expenses = df[df["částka platby"] < 0]

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
        text_auto=".2s",
        title="TOP 10 příjemců plateb",
    )

    fig.update_layout(
        height=420,
        yaxis=dict(categoryorder="total ascending"),
    )

    return fig


def cashflow_chart(df):

    tmp = df.copy()

    tmp["Měsíc"] = (
        tmp["datum zaúčtování"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        tmp.groupby("Měsíc")["částka platby"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Měsíc",
        y="částka platby",
        markers=True,
        title="Cashflow po měsících",
    )

    fig.update_layout(height=420)

    return fig


def daily_expense_chart(df):

    expenses = df[df["částka platby"] < 0].copy()

    daily = (
        expenses.groupby("datum zaúčtování")["částka platby"]
        .sum()
        .abs()
        .reset_index()
    )

    fig = px.bar(
        daily,
        x="datum zaúčtování",
        y="částka platby",
        title="Denní výdaje",
    )

    fig.update_layout(height=420)

    return fig
