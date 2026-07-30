import streamlit as st

from utils.loader import load_file
from utils.metrics import calculate_metrics
from utils.charts import (
    balance_chart,
    category_chart,
    monthly_chart,
    top_suppliers_chart,
    cashflow_chart,
    cumulative_cashflow_chart,
    weekday_expense_chart,
    category_trend_chart,
)
from utils.filters import filter_data
from utils.categories import categorize


st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- CSS ----------

try:
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
except FileNotFoundError:
    pass


def czk(value):
    return (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", " ")
        + " Kč"
    )


st.title("📊 Business Cockpit")
st.caption("Finanční dashboard")

uploaded_file = st.file_uploader(
    "Nahraj CSV nebo XLSX",
    type=["csv", "xlsx"],
)

if uploaded_file:

    df = load_file(uploaded_file)

    df = categorize(df)

    df = filter_data(df)

    # zpřístupnění pro pages/*
    st.session_state["df"] = df

    metrics = calculate_metrics(df)

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Stav účtu",
        czk(metrics["balance"]),
    )

    c2.metric(
        "📈 Příjmy",
        czk(metrics["income"]),
    )

    c3.metric(
        "📉 Výdaje",
        czk(metrics["expense"]),
    )

    c4.metric(
        "📊 Cashflow",
        czk(metrics["cashflow"]),
        f"{metrics['savings_rate']} %",
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "📄 Transakcí",
        metrics["transactions"],
    )

    c6.metric(
        "📅 Aktivních dní",
        metrics["active_days"],
    )

    c7.metric(
        "⬆️ Nejvyšší příjem",
        czk(metrics["biggest_income"]),
    )

    c8.metric(
        "⬇️ Nejvyšší výdaj",
        czk(metrics["biggest_expense"]),
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Dashboard",
            "📈 Analýzy",
            "📄 Transakce",
        ]
    )

    with tab1:

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

            st.plotly_chart(
                cumulative_cashflow_chart(df),
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

            st.plotly_chart(
                cashflow_chart(df),
                use_container_width=True,
            )

    with tab2:

        left, right = st.columns(2)

        with left:

            st.plotly_chart(
                weekday_expense_chart(df),
                use_container_width=True,
            )

        with right:

            st.plotly_chart(
                category_trend_chart(df),
                use_container_width=True,
            )

        st.divider()

        st.subheader("🤖 AI CFO")

        if metrics["cashflow"] > 0:
            st.success(
                "Cashflow je kladné. Firma vytváří přebytek hotovosti."
            )
        else:
            st.error(
                "Cashflow je záporné. Výdaje převyšují příjmy."
            )

        if metrics["income"] > 0:

            ratio = (
                metrics["expense"]
                / metrics["income"]
            )

            if ratio > 0.80:
                st.warning(
                    "Výdaje tvoří více než 80 % příjmů."
                )

        if (
            metrics["avg_expense"] > 0
            and metrics["biggest_expense"]
            > metrics["avg_expense"] * 3
        ):
            st.info(
                "Byla nalezena mimořádně vysoká výdajová transakce."
            )

        st.markdown("### Doporučení")

        recommendations = []

        if metrics["cashflow"] < 0:
            recommendations.append(
                "• Zaměřte se na snížení provozních nákladů."
            )

        if metrics["savings_rate"] < 10:
            recommendations.append(
                "• Nízká míra úspor. Doporučujeme analyzovat hlavní nákladové položky."
            )

        if metrics["transactions"] > 500:
            recommendations.append(
                "• Vysoký počet transakcí. Zvažte jejich automatickou kategorizaci."
            )

        if not recommendations:
            recommendations.append(
                "• Finanční situace je stabilní."
            )

        for item in recommendations:
            st.markdown(item)

    with tab3:

        columns = [
            "datum zaúčtování",
            "Kategorie",
            "částka platby",
            "protistrana",
            "popis transakce",
        ]

        existing = [
            c
            for c in columns
            if c in df.columns
        ]

        st.dataframe(
            df[existing]
            .sort_values(
                "datum zaúčtování",
                ascending=False,
            ),
            use_container_width=True,
            hide_index=True,
        )

else:

    st.info(
        "Nahraj bankovní výpis ve formátu CSV nebo XLSX."
    )
