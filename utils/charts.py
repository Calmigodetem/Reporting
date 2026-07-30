import plotly.express as px


def balance_chart(df):
    fig = px.line(
        df.sort_values("datum zaúčtování"),
        x="datum zaúčtování",
        y="zůstatek",
        title="Vývoj zůstatku"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def category_chart(df):

    expenses = df[df["částka platby"] < 0].copy()

    summary = (
        expenses.groupby("Kategorie")["částka platby"]
        .sum()
        .abs()
        .reset_index()
    )

    fig = px.pie(
        summary,
        names="Kategorie",
        values="částka platby",
        title="Výdaje podle kategorií"
    )

    return fig
