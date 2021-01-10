import base64
import datetime
import io
import pandas as pd
from parse_number import parseNumber

# utility functions
def parse_data(filename, contents="", isFileOnly=None, transpose=False):
    """
    -> parse uploaded .csv | .xlsx data
    -> [isFileOnly] if True will read from file only (default onStart file to load data)
    :param contents:
    :param filename:
    :param isFileOnly
    :return: pandas dataframe
    """

    if isFileOnly:
        try:
            if "csv" in filename:
                # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(
                    filename,
                    index_col=False,
                )

            elif "xls" in filename:
                # Assume that the user uploaded an excel file
                pd.read_excel(filename)

        except Exception as e:
            print(f"[ERROR] Error processing file: `{filename}`. {e}")

            # TODO: Add a bootstrap error button or toast
            # return html.Div(["There was an error processing this file."])

    else:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)

        try:
            if "csv" in filename:
                # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
                df = df.fillna(method="ffill")

            elif "xls" in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
                df = df.fillna(method="ffill")

        except Exception as e:
            print(f"[ERROR] Error processing file: `{filename}`. {e}")

    # TODO: Add a bootstrap error button or toast
    # return html.Div(["There was an error processing this file."])

    # Transpose to make first column into rows
    # set default file first column as df header for easy referencing
    if transpose:
        df2 = df.T

    else:
        df2 = df

    # header = df2.iloc[0]
    # df2 = df2[1:]
    # df2.columns = header

    return df2


def calc_percentage_change(html, latestValue, prevValue):
    # return a Div component styled for red | green

    perc_change = 0
    color = "grey"

    perc_ch = (latestValue - prevValue) / prevValue

    signedPercChange = perc_ch * 100

    if signedPercChange < 0:
        color = "red"

    if signedPercChange > 0:
        color = "green"

    perc_change = round(signedPercChange, 2)

    res = (html.H5(f"{abs(perc_change)} %", style={"color": color, "size": 25}),)
    return res


def parseStrNumToNumeric(listData):
    parsed = []
    for strNum in listData:
        parsed.append(parseNumber(strNum))

    return parsed


def parse_summary(html, years_list, selectedYear, df):
    # constants index where needed data is
    BUDGET_DEF = 4
    IMPORTS = 13
    EXPORTS = 12
    NET_IMPORTS = 11
    INF_RATE = 16
    GRO_RATE = 15
    GVT_EXP = 14
    PRIV_INV = 9

    if selectedYear in years_list:
        try:
            latestData = parseStrNumToNumeric((df[f"{selectedYear}"]))
            prevYear = int(selectedYear) - 1
            
            try:
                prevData = parseStrNumToNumeric(list(df[f"{prevYear}"]))

            except Exception as err:
                print('[-] Error getting prev year data: ', prevYear)
                prevData = parseStrNumToNumeric(list(df[f"{selectedYear}"]))

            budgetDef = (html.H1(latestData[BUDGET_DEF], style={"size": 40}),)
            budgChange = calc_percentage_change(
                html, latestData[BUDGET_DEF], prevData[BUDGET_DEF]
            )

            imports = (html.H1(latestData[IMPORTS], style={"size": 40}),)
            importsCh = calc_percentage_change(
                html, latestData[IMPORTS], prevData[IMPORTS]
            )

            exports = (html.H1(latestData[EXPORTS], style={"size": 40}),)
            exportsCh = calc_percentage_change(
                html, latestData[EXPORTS], prevData[EXPORTS]
            )

            netImports = (html.H1(latestData[NET_IMPORTS], style={"size": 40}),)
            netImportsCh = calc_percentage_change(
                html, latestData[NET_IMPORTS], prevData[NET_IMPORTS]
            )

            infRate = (html.H1(f"{latestData[INF_RATE]} %", style={"size": 40}),)
            infRateCh = calc_percentage_change(
                html, latestData[INF_RATE], prevData[INF_RATE]
            )

            groRate = (html.H1(f"{latestData[GRO_RATE]} %", style={"size": 40}),)
            groRateCh = calc_percentage_change(
                html, latestData[GRO_RATE], prevData[GRO_RATE]
            )

            gvtExp = (html.H1(f"{latestData[GVT_EXP]} %", style={"size": 40}),)
            gvtExpCh = calc_percentage_change(
                html, latestData[GVT_EXP], prevData[GVT_EXP]
            )

            privInv = (html.H1(f"{latestData[PRIV_INV]} %", style={"size": 40}),)
            privInvCh = calc_percentage_change(
                html, latestData[PRIV_INV], prevData[PRIV_INV]
            )

        except Exception as err:
            budgetDef = "N/A"
            budgChange = "n/a"

            imports = "N/A"
            importsCh = "n/a"

            exports = "N/A"
            exportsCh = "n/a"

            netImports = "N/A"
            netImportsCh = "n/a"

            infRate = "N/A"
            infRateCh = "n/a"

            groRate = "N/A"
            groRateCh = "n/a"

            gvtExp = "N/A"
            gvtExpCh = "n/a"

            privInv = "N/A"
            privInvCh = "n/a"

            print("Error: ", err)

    return (
        f"{selectedYear}",
        budgetDef,
        budgChange,
        imports,
        importsCh,
        exports,
        exportsCh,
        netImports,
        netImportsCh,
        infRate,
        infRateCh,
        groRate,
        groRateCh,
        gvtExp,
        gvtExpCh,
        privInv,
        privInvCh,
    )
