import streamlit as st


def filter_data(df):

    years = sorted(df["datum zaúčtování"].dt.year.dropna().unique())

    selected_year = st.sidebar.selectbox(
        "Rok",
        years,
        index=len(years) - 1
    )

    months = ["Vše"] + list(range(1, 13))

    selected_month = st.sidebar.selectbox(
        "Měsíc",
        months
    )

    filtered = df[df["datum zaúčtování"].dt.year == selected_year]

    if selected_month != "Vše":
        filtered = filtered[
            filtered["datum zaúčtování"].dt.month == selected_month
        ]

    return filtered
