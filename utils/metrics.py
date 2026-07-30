import pandas as pd


def calculate_metrics(df):

    balance = (
        df["zůstatek"].iloc[-1]
        if "zůstatek" in df.columns and len(df)
        else 0
    )

    income = (
        df.loc[
            df["částka platby"] > 0,
            "částka platby",
        ].sum()
    )

    expense = abs(
        df.loc[
            df["částka platby"] < 0,
            "částka platby",
        ].sum()
    )

    cashflow = income - expense

    transactions = len(df)

    avg_income = (
        df.loc[
            df["částka platby"] > 0,
            "částka platby",
        ].mean()
        if income
        else 0
    )

    avg_expense = abs(
        df.loc[
            df["částka platby"] < 0,
            "částka platby",
        ].mean()
    ) if expense else 0

    biggest_income = (
        df.loc[
            df["částka platby"] > 0,
            "částka platby",
        ].max()
        if income
        else 0
    )

    biggest_expense = abs(
        df.loc[
            df["částka platby"] < 0,
            "částka platby",
        ].min()
    ) if expense else 0

    active_days = (
        df["datum zaúčtování"]
        .dt.date
        .nunique()
    )

    return {
        "balance": balance,
        "income": income,
        "expense": expense,
        "cashflow": cashflow,
        "transactions": transactions,
        "avg_income": avg_income,
        "avg_expense": avg_expense,
        "biggest_income": biggest_income,
        "biggest_expense": biggest_expense,
        "active_days": active_days,
    }
