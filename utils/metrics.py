import pandas as pd


def calculate_metrics(df):

    income = (
        df.loc[df["částka platby"] > 0, "částka platby"]
        .sum()
    )

    expense = (
        abs(
            df.loc[df["částka platby"] < 0, "částka platby"]
            .sum()
        )
    )

    cashflow = income - expense

    balance = (
        df.sort_values("datum zaúčtování")
        .iloc[-1]["zůstatek"]
    )

    transactions = len(df)

    active_days = (
        df["datum zaúčtování"]
        .dt.date
        .nunique()
    )

    incomes = df.loc[
        df["částka platby"] > 0,
        "částka platby",
    ]

    expenses = abs(
        df.loc[
            df["částka platby"] < 0,
            "částka platby",
        ]
    )

    biggest_income = (
        incomes.max()
        if not incomes.empty
        else 0
    )

    biggest_expense = (
        expenses.max()
        if not expenses.empty
        else 0
    )

    avg_income = (
        incomes.mean()
        if not incomes.empty
        else 0
    )

    avg_expense = (
        expenses.mean()
        if not expenses.empty
        else 0
    )

    median_expense = (
        expenses.median()
        if not expenses.empty
        else 0
    )

    median_income = (
        incomes.median()
        if not incomes.empty
        else 0
    )

    savings_rate = (
        round((cashflow / income) * 100, 1)
        if income > 0
        else 0
    )

    return {
        "income": float(income),
        "expense": float(expense),
        "cashflow": float(cashflow),
        "balance": float(balance),
        "transactions": int(transactions),
        "active_days": int(active_days),
        "biggest_income": float(biggest_income),
        "biggest_expense": float(biggest_expense),
        "avg_income": float(avg_income),
        "avg_expense": float(avg_expense),
        "median_income": float(median_income),
        "median_expense": float(median_expense),
        "savings_rate": float(savings_rate),
    }
