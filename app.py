import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Business Cockpit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Cockpit")

uploaded_file = st.file_uploader(
    "Nahraj CSV nebo Excel",
    type=["csv","xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(
            uploaded_file,
            sep=";",
            encoding="cp1250"
        )
    else:
        df = pd.read_excel(uploaded_file)

    # převod datumu
    df["datum zaúčtování"] = pd.to_datetime(
        df["datum zaúčtování"],
        dayfirst=True,
        errors="coerce"
    )

    # převod čísel
    for col in ["částka platby","zůstatek"]:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",",".")
            .astype(float)
        )

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "💰 Aktuální stav",
        f"{df.iloc[0]['zůstatek']:,.0f} Kč"
    )

    col2.metric(
        "📄 Transakcí",
        len(df)
    )

    col3.metric(
        "⬆ Nejvyšší příjem",
        f"{df['částka platby'].max():,.0f} Kč"
    )

    col4.metric(
        "⬇ Nejvyšší výdaj",
        f"{df['částka platby'].min():,.0f} Kč"
    )

    st.line_chart(
        df.set_index("datum zaúčtování")["zůstatek"]
    )

    st.dataframe(df)
