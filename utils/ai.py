import pandas as pd


def financial_health(metrics):

    score = 100

    if metrics["cashflow"] < 0:
        score -= 35

    if metrics["income"] > 0:
        ratio = metrics["expense"] / metrics["income"]

        if ratio > 0.90:
            score -= 30
        elif ratio > 0.80:
            score -= 15

    if metrics["savings_rate"] < 10:
        score -= 10

    return max(score, 0)


def recommendations(df, metrics):

    rec = []

    if metrics["cashflow"] < 0:
        rec.append(
            "Cashflow je záporné. Zaměřte se na snížení nákladů nebo zvýšení příjmů."
        )

    expenses = (
        df[df["částka platby"] < 0]
        .groupby("Kategorie")["částka platby"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    if len(expenses):

        rec.append(
            f"Nejvyšší nákladová kategorie je **{expenses.index[0]}** ({expenses.iloc[0]:,.0f} Kč)."
        )

    suppliers = (
        df[df["částka platby"] < 0]
        .groupby("protistrana")["částka platby"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    if len(suppliers):

        rec.append(
            f"Největší dodavatel je **{suppliers.index[0]}**."
        )

    if metrics["savings_rate"] < 20:
        rec.append(
            "Míra úspor je nízká. Cílem by mělo být alespoň 20 %."
        )

    if not rec:
        rec.append(
            "Finance vypadají zdravě. Pokračujte ve stejném trendu."
        )

    return rec


def monthly_summary(df):

    tmp = df.copy()

    tmp["Měsíc"] = (
        tmp["datum zaúčtování"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        tmp.groupby("Měsíc")["částka platby"]
        .agg(
            Příjmy=lambda x: x[x > 0].sum(),
            Výdaje=lambda x: abs(x[x < 0].sum()),
            Cashflow="sum",
        )
        .fillna(0)
        .reset_index()
    )

    return result
