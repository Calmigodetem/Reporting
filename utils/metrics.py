def calculate_metrics(df):

    balance = df["zůstatek"].iloc[-1]

    income = df[df["částka platby"] > 0]["částka platby"].sum()

    expense = abs(
        df[df["částka platby"] < 0]["částka platby"].sum()
    )

    cashflow = income - expense

    return {
        "balance": balance,
        "income": income,
        "expense": expense,
        "cashflow": cashflow,
    }
