from io import BytesIO

import pandas as pd


def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter",
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Transakce",
            index=False,
        )

        workbook = writer.book
        worksheet = writer.sheets["Transakce"]

        money = workbook.add_format(
            {
                "num_format": '# ##0.00 "Kč"',
            }
        )

        date = workbook.add_format(
            {
                "num_format": "dd.mm.yyyy",
            }
        )

        for i, col in enumerate(df.columns):

            width = max(
                len(str(col)),
                df[col].astype(str).str.len().max(),
            )

            worksheet.set_column(
                i,
                i,
                min(width + 3, 40),
            )

        if "datum zaúčtování" in df.columns:

            idx = df.columns.get_loc(
                "datum zaúčtování"
            )

            worksheet.set_column(
                idx,
                idx,
                14,
                date,
            )

        if "částka platby" in df.columns:

            idx = df.columns.get_loc(
                "částka platby"
            )

            worksheet.set_column(
                idx,
                idx,
                18,
                money,
            )

        if "zůstatek" in df.columns:

            idx = df.columns.get_loc(
                "zůstatek"
            )

            worksheet.set_column(
                idx,
                idx,
                18,
                money,
            )

    output.seek(0)

    return output


def export_csv(df):

    return df.to_csv(
        index=False,
        sep=";",
    ).encode("utf-8-sig")
