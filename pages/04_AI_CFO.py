import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI CFO",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI CFO")

if "df" not in st.session_state:
    st.warning("Nejprve nahraj data na hlavní stránce.")
    st.stop()

df = st.session_state["df"].copy()

income = df.loc[df["částka platby"] > 0, "částka platby"].sum()
expense = abs(df.loc[df["částka platby"] < 0, "částka platby"].sum())
cashflow = income - expense

expenses = (
    df[df["částka platby"] < 0]
    .groupby("Kategorie")["částka platby"]
    .sum()
    .abs()
    .sort_values(ascending=False)
)

largest_supplier = (
    df[df["částka platby"] < 0]
    .groupby("protistrana")["částka platby"]
    .sum()
    .abs()
    .sort_values(ascending=False)
)

st.subheader("Finanční zdraví")

if income > 0:

    ratio = expense / income

    if ratio < 0.60:
        st.success("🟢 Výdaje jsou velmi dobře pod kontrolou.")

    elif ratio < 0.80:
        st.info("🟡 Výdaje jsou zdravé, ale je prostor pro další optimalizaci.")

    elif ratio < 1:
        st.warning("🟠 Výdaje jsou vysoké. Doporučujeme jejich revizi.")

    else:
        st.error("🔴 Výdaje převyšují příjmy.")

st.divider()

st.subheader("Doporučení")

recommendations = []

if cashflow < 0:
    recommendations.append(
        "• Zaměřte se na zvýšení příjmů nebo snížení nákladů."
    )

if not expenses.empty:

    top_category = expenses.index[0]

    recommendations.append(
        f"• Nejvíce prostředků odchází do kategorie **{top_category}**."
    )

if not largest_supplier.empty:

    supplier = largest_supplier.index[0]

    recommendations.append(
        f"• Největší dodavatel je **{supplier}**."
    )

if income > 0:

    savings = (cashflow / income) * 100

    recommendations.append(
        f"• Míra úspor činí **{savings:.1f} %**."
    )

for item in recommendations:
    st.markdown(item)

st.divider()

st.subheader("TOP 10 kategorií")

if not expenses.empty:

    table = expenses.reset_index()
    table.columns = ["Kategorie", "Výdaje"]

    st.dataframe(
        table.style.format(
            {"Výdaje": "{:,.0f} Kč"}
        ),
        use_container_width=True,
        hide_index=True,
    )

st.subheader("TOP 10 dodavatelů")

if not largest_supplier.empty:

    supplier_table = largest_supplier.head(10).reset_index()
    supplier_table.columns = [
        "Dodavatel",
        "Výdaje",
    ]

    st.dataframe(
        supplier_table.style.format(
            {"Výdaje": "{:,.0f} Kč"}
        ),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.subheader("Shrnutí")

summary = f"""
### Přehled

- Příjmy: **{income:,.0f} Kč**
- Výdaje: **{expense:,.0f} Kč**
- Cashflow: **{cashflow:,.0f} Kč**
- Počet transakcí: **{len(df)}**
"""

st.markdown(summary)
