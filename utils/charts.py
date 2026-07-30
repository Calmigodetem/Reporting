import plotly.express as px


def balance_chart(df):

    fig = px.line(
        df,
        x="datum zaúčtování",
        y="zůstatek",
        markers=True,
        title="Vývoj zůstatku"
    )

    fig.update_layout(
        xaxis_title="Datum",
        yaxis_title="Kč",
        height=450
    )

    return fig
