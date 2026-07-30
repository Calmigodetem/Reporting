import streamlit as st


def filter_data(df):

    with st.sidebar:

        st.subheader("Filtry")

        min_date = df["datum zaúčtování"].min().date()
        max_date = df["datum zaúčtování"].max().date()

        date_range = st.date_input(
            "Období",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if len(date_range) == 2:
            start_date, end_date = date_range

            df = df[
                (df["datum zaúčtování"].dt.date >= start_date)
                & (df["datum zaúčtování"].dt.date <= end_date)
            ]

        if "Kategorie" in df.columns:

            categories = sorted(
                df["Kategorie"]
                .dropna()
                .unique()
                .tolist()
            )

            selected = st.multiselect(
                "Kategorie",
                categories,
                default=categories,
            )

            if selected:
                df = df[
                    df["Kategorie"].isin(selected)
                ]

        if "protistrana" in df.columns:

            partners = sorted(
                df["protistrana"]
                .fillna("")
                .unique()
                .tolist()
            )

            selected = st.multiselect(
                "Protistrana",
                partners,
                default=partners,
            )

            if selected:
                df = df[
                    df["protistrana"].isin(selected)
                ]

        min_amount = float(df["částka platby"].min())
        max_amount = float(df["částka platby"].max())

        amount = st.slider(
            "Částka",
            min_value=min_amount,
            max_value=max_amount,
            value=(min_amount, max_amount),
        )

        df = df[
            (df["částka platby"] >= amount[0])
            & (df["částka platby"] <= amount[1])
        ]

        search = st.text_input(
            "Hledat",
            placeholder="Dodavatel nebo popis...",
        )

        if search:

            text = (
                df["protistrana"]
                .fillna("")
                .astype(str)
                + " "
                + df["popis transakce"]
                .fillna("")
                .astype(str)
            )

            df = df[
                text.str.contains(
                    search,
                    case=False,
                    na=False,
                )
            ]

    return df.reset_index(drop=True)
