import pandas as pd
import plotly.express as px


def _layout(fig, height=420):

    fig.update_layout(
        height=height,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10,
        ),
        template="plotly_white",
        hovermode="x unified",
        legend_title=None,
    )

    return fig


def balance_chart(df):

    fig = px.line(
        df.sort_values("datum zaúčtování"),
        x="datum zaúčtování",
        y="zůstatek",
        markers=True,
        title="Vývoj zůstatku",
    )

    return _layout(fig)


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

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    return _layout(fig)


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

    return _layout(fig)


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
        title="TOP 10 příjemců",
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    return _layout(fig)


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
        title="Cashflow",
    )

    return _layout(fig)


def daily_expense_chart(df):

    expenses = df[df["částka platby"] < 0]

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

    return _layout(fig)


def cumulative_cashflow_chart(df):

    tmp = (
        df.sort_values("datum zaúčtování")
        .copy()
    )

    tmp["Kumulované cashflow"] = (
        tmp["částka platby"].cumsum()
    )

    fig = px.area(
        tmp,
        x="datum zaúčtování",
        y="Kumulované cashflow",
        title="Kumulované cashflow",
    )

    return _layout(fig)


def weekday_expense_chart(df):

    expenses = df[df["částka platby"] < 0].copy()

    mapping = {
        0: "Po",
        1: "Út",
        2: "St",
        3: "Čt",
        4: "Pá",
        5: "So",
        6: "Ne",
    }

    expenses["Den"] = (
        expenses["datum zaúčtování"]
        .dt.dayofweek
        .map(mapping)
    )

    summary = (
        expenses.groupby("Den")["částka platby"]
        .sum()
        .abs()
        .reindex(
            [
                "Po",
                "Út",
                "St",
                "Čt",
                "Pá",
                "So",
                "Ne",
            ]
        )
        .reset_index()
    )

    fig = px.bar(
        summary,
        x="Den",
        y="částka platby",
        text_auto=".2s",
        title="Výdaje podle dne",
    )

    return _layout(fig)


def category_trend_chart(df):

    expenses = df[df["částka platby"] < 0].copy()

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

    fig = px.line(
        trend,
        x="Měsíc",
        y="částka platby",
        color="Kategorie",
        markers=True,
        title="Trend kategorií",
    )

    return _layout(fig)


def income_vs_expense_chart(df):

    tmp = df.copy()

    tmp["Směr"] = tmp["částka platby"].apply(
        lambda x: "Příjem"
        if x > 0
        else "Výdaj"
    )

    tmp["Hodnota"] = (
        tmp["částka platby"].abs()
    )

    fig = px.histogram(
        tmp,
        x="Kategorie",
        y="Hodnota",
        color="Směr",
        barmode="group",
        title="Příjmy vs výdaje podle kategorií",
    )

    return _layout(fig)
