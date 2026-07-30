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
from utils.export import export_excel, export_csv


st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


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
    "Nahraj bankovní výpis",
    type=["csv", "xlsx"],
)


if uploaded_file:

    df = load_file(uploaded_file)
    df = categorize(df)
    df = filter_data(df)

    st.session_state["df"] = df

    metrics = calculate_metrics(df)

    cols = st.columns(4)

    cols[0].metric("💰 Stav účtu", czk(metrics["balance"]))
    cols[1].metric("📈 Příjmy", czk(metrics["income"]))
    cols[2].metric("📉 Výdaje", czk(metrics["expense"]))
    cols[3].metric("📊 Cashflow", czk(metrics["cashflow"]))

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["📊 Dashboard", "📈 Analýzy", "📄 Transakce"]
    )

    with tab1:

        left, right = st.columns(2)

        with left:
            st.plotly_chart(balance_chart(df), use_container_width=True)
            st.plotly_chart(monthly_chart(df), use_container_width=True)
            st.plotly_chart(
                cumulative_cashflow_chart(df),
                use_container_width=True,
            )

        with right:
            st.plotly_chart(category_chart(df), use_container_width=True)
            st.plotly_chart(top_suppliers_chart(df), use_container_width=True)
            st.plotly_chart(cashflow_chart(df), use_container_width=True)

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

        st.subheader("🤖 AI CFO")

        if metrics["cashflow"] > 0:
            st.success("Cashflow je kladné.")
        else:
            st.warning("Cashflow je záporné.")

    with tab3:

        st.dataframe(
            df.sort_values(
                "datum zaúčtování",
                ascending=False,
            ),
            use_container_width=True,
            hide_index=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            st.download_button(
                "📗 Excel",
                export_excel(df),
                file_name="business_cockpit.xlsx",
            )

        with c2:
            st.download_button(
                "📄 CSV",
                export_csv(df),
                file_name="business_cockpit.csv",
            )

else:

    st.info("Nahraj CSV nebo XLSX bankovní výpis.")
