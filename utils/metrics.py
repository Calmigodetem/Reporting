import pandas as pd


def calculate_metrics(df):

    balance = df["zůstatek"].iloc[-1]

    income = df[df["částka platby"] > 0]["částka platby"].sum()

    expense = abs(
        df[df["částka platby"] < 0]["částka platby"].sum()
    )

    cashflow = income - expense

    transactions = len(df)

    avg_income = (
        df[df["částka platby"] > 0]["částka platby"].mean()
        if income > 0
        else 0
    )

    avg_expense = abs(
        df[df["částka platby"] < 0]["částka platby"].mean()
    ) if expense > 0 else 0

    return {
        "balance": balance,
        "income": income,
        "expense": expense,
        "cashflow": cashflow,
        "transactions": transactions,
        "avg_income": avg_income,
        "avg_expense": avg_expense,
    }
