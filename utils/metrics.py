import pandas as pd


def calculate_metrics(df):

    balance = (
        float(df["zůstatek"].iloc[-1])
        if len(df)
        else 0
    )

    income = float(
        df.loc[
            df["částka platby"] > 0,
            "částka platby",
        ].sum()
    )

    expense = abs(
        float(
            df.loc[
                df["částka platby"] < 0,
                "částka platby",
            ].sum()
        )
    )

    cashflow = income - expense

    transactions = len(df)

    avg_income = (
        float(
            df.loc[
                df["částka platby"] > 0,
                "částka platby",
            ].mean()
        )
        if income
        else 0
    )

    avg_expense = (
        abs(
            float(
                df.loc[
                    df["částka platby"] < 0,
                    "částka platby",
                ].mean()
            )
        )
        if expense
        else 0
    )

    biggest_income = (
        float(
            df.loc[
                df["částka platby"] > 0,
                "částka platby",
            ].max()
        )
        if income
        else 0
    )

    biggest_expense = (
        abs(
            float(
                df.loc[
                    df["částka platby"] < 0,
                    "částka platby",
                ].min()
            )
        )
        if expense
        else 0
    )

    active_days = (
        df["datum zaúčtování"]
        .dt.date
        .nunique()
    )

    income_transactions = int(
        (df["částka platby"] > 0).sum()
    )

    expense_transactions = int(
        (df["částka platby"] < 0).sum()
    )

    average_daily_expense = (
        expense / active_days
        if active_days
        else 0
    )

    average_daily_income = (
        income / active_days
        if active_days
        else 0
    )

    savings_rate = (
        round(
            (cashflow / income) * 100,
            1,
        )
        if income
        else 0
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
        "income_transactions": income_transactions,
        "expense_transactions": expense_transactions,
        "average_daily_income": average_daily_income,
        "average_daily_expense": average_daily_expense,
        "savings_rate": savings_rate,
    }
