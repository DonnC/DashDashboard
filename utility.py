import base64
import datetime
import io
import pandas as pd


# utility functions
def parse_data(filename, contents='', isFileOnly=None):
    '''
    -> parse uploaded .csv | .xlsx data
    -> [isFileOnly] if True will read from file only (default onStart file to load data)
    :param contents:
    :param filename:
    :param isFileOnly
    :return: pandas dataframe
    '''

    if (isFileOnly):
        try:
            if "csv" in filename:
                # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(filename, index_col=False,)

            elif "xls" in filename:
                # Assume that the user uploaded an excel file
                pd.read_excel(filename)

        except Exception as e:
            print(f'[ERROR] Error processing file: `{filename}`. {e}')

            # TODO: Add a bootstrap error button or toast
            # return html.Div(["There was an error processing this file."])

    else:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)

        try:
            if "csv" in filename:
                # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            elif "xls" in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))

        except Exception as e:
            print(f'[ERROR] Error processing file: `{filename}`. {e}')

    # TODO: Add a bootstrap error button or toast
    # return html.Div(["There was an error processing this file."])


    # Transpose to make first column into rows
    # set default file first column as df header for easy referencing
    df2 = df.T
    #header = df2.iloc[0]
    #df2 = df2[1:]
    #df2.columns = header

    return df2
