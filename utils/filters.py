import streamlit as st


def filter_data(df):

    years = sorted(
        df["datum zaúčtování"]
        .dt.year
        .dropna()
        .unique()
    )

    selected_year = st.sidebar.selectbox(
        "Rok",
        years,
        index=len(years) - 1,
    )

    months = ["Vše"] + list(range(1, 13))

    selected_month = st.sidebar.selectbox(
        "Měsíc",
        months,
    )

    transaction_type = st.sidebar.selectbox(
        "Typ transakcí",
        [
            "Vše",
            "Příjmy",
            "Výdaje",
        ],
    )

    categories = (
        ["Vše"]
        + sorted(
            df["Kategorie"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_category = st.sidebar.selectbox(
        "Kategorie",
        categories,
    )

    min_amount = float(df["částka platby"].min())
    max_amount = float(df["částka platby"].max())

    amount_range = st.sidebar.slider(
        "Rozsah částky",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount),
    )

    search = st.sidebar.text_input(
        "Hledat protistranu",
    )

    filtered = df[
        df["datum zaúčtování"].dt.year == selected_year
    ]

    if selected_month != "Vše":
        filtered = filtered[
            filtered["datum zaúčtování"].dt.month
            == selected_month
        ]

    if transaction_type == "Příjmy":
        filtered = filtered[
            filtered["částka platby"] > 0
        ]

    elif transaction_type == "Výdaje":
        filtered = filtered[
            filtered["částka platby"] < 0
        ]

    filtered = filtered[
        (
            filtered["částka platby"]
            >= amount_range[0]
        )
        &
        (
            filtered["částka platby"]
            <= amount_range[1]
        )
    ]

    if selected_category != "Vše":
        filtered = filtered[
            filtered["Kategorie"]
            == selected_category
        ]

    if search:

        filtered = filtered[
            filtered["protistrana"]
            .fillna("")
            .str.contains(
                search,
                case=False,
            )
        ]

    filtered = filtered.sort_values(
        "datum zaúčtování",
        ascending=False,
    )

    return filtered
