"""
@author: <https://github.com/DonnC>
@created: 08 Jan 2021
@project: dash dashboard
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_auth
import dash

from utility import parse_data, parse_summary
from app_users import USERNAME_PASSWORD_PAIRS

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# load static data
# annual international trade stats
dfAit = parse_data(filename="data/ait.csv", isFileOnly=True, transpose=True)

# economic indicators
dfEco = parse_data(filename="data/eco-ind.csv", isFileOnly=True)

uploadAit = dcc.Upload(
    id="upload-ait-data",
    children=html.Div("Upload Trade Stats `.csv` File"),
    multiple=False,
)
uploadEind = dcc.Upload(
    id="upload-ei-data",
    children=html.Div("Upload Economic Indicators `.csv` File"),
    multiple=False,
)

jumbtronHeader = dbc.Jumbotron(
    [
        html.H1("Dashboard", className="display-6"),
        html.P(
            "Analyse and visualize trade deficit GDP and inflation. "
            "All intepreted from 2 variable exports and imports. "
            "from two industries: Primary Industry and Secondary Industry",
            className="lead",
        ),
        dbc.Row(
            [
                dbc.Button(
                    uploadAit,
                    size="md",
                    className="mr-1",
                ),
                dbc.Button(
                    uploadEind,
                    size="md",
                    className="mr-1",
                ),
            ],
            justify="end",
        ),
    ],
)


def summaryYearItems(yearList):
    items = []
    yearList.remove("Year")

    for year in yearList:
        items.append(
            {
                "value": f"{year}",
                "label": f"{year}",
            }
        )

    return items


def summaryCard(title, valueID, percChangeID):
    """
    create a summary card
    :param title: title of card tile
    :param valueID: id of the value being dynamically changed
    :param percChangeID: id of the percentage change
    :return: dbc.Card component
    """

    summaryCard = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(title, style={"color": "grey"}),
                    # html.H1("2382", id=valueID, style={'size': 40}),
                    html.Div(id=valueID),
                    html.Div(id=percChangeID),
                    # html.H5("3.23%", id=percChangeID, style={'color': 'grey', 'size': 25}),
                    html.H6("Since previous year", style={"color": "grey", "size": 20}),
                ]
            )
        ]
    )
    return summaryCard


def getFirstRowSummaryCards():
    cards = []

    budgetDeficit = summaryCard(
        title="BUDGET DEFICIT", valueID="budget-deficit", percChangeID="bd-perc-change"
    )
    imports_ = summaryCard(
        title="IMPORTS", valueID="imports", percChangeID="imports-perc-change"
    )
    exports_ = summaryCard(
        title="EXPORTS", valueID="exports", percChangeID="exports-perc-change"
    )
    netImports = summaryCard(
        title="NET IMPORTS",
        valueID="net-imports",
        percChangeID="net-imports-perc-change",
    )

    cards.append(budgetDeficit)
    cards.append(imports_)
    cards.append(exports_)
    cards.append(netImports)

    return cards


def getSecondRowSummaryCards():
    cards = []

    inflationRatesAnn = summaryCard(
        title="INFLATION RATE ANNUAL CHANGE",
        valueID="inflation-rate",
        percChangeID="ira-perc-change",
    )
    realGroRate = summaryCard(
        title="REAL GROWTH RATE / ANNUM",
        valueID="growth-rate",
        percChangeID="rgr-perc-change",
    )
    gvtExpToGdp = summaryCard(
        title="GVT EXPENDITURE-GDP RATIO",
        valueID="gvt-expenditure",
        percChangeID="getgdp-perc-change",
    )
    privInvGdp = summaryCard(
        title="PVT INVESTMENT / GDP",
        valueID="private-inv",
        percChangeID="pigdp-imports-perc-change",
    )

    cards.append(inflationRatesAnn)
    cards.append(realGroRate)
    cards.append(gvtExpToGdp)
    cards.append(privInvGdp)

    return cards


summaryCard = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        "Summary for Year:",
                                        className="card-text",
                                    ),
                                    width=4,
                                ),
                                dbc.Col(html.Div(id="summary-year-value"), width=4),
                            ],
                            justify="start",
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="summary-year-filter",
                                value=list(dfEco.columns.values)[-1],
                                options=summaryYearItems(list(dfEco.columns.values)),
                                clearable=False,
                                placeholder="Select Year",
                            ),
                            width={"size": 4},
                        ),
                    ],
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    getFirstRowSummaryCards()[0],
                                ),
                                dbc.Col(
                                    getFirstRowSummaryCards()[1],
                                ),
                                dbc.Col(
                                    getFirstRowSummaryCards()[2],
                                ),
                                dbc.Col(
                                    getFirstRowSummaryCards()[3],
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    getSecondRowSummaryCards()[0],
                                ),
                                dbc.Col(
                                    getSecondRowSummaryCards()[1],
                                ),
                                dbc.Col(
                                    getSecondRowSummaryCards()[2],
                                ),
                                dbc.Col(
                                    getSecondRowSummaryCards()[3],
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                ),
            ],
        ),
    ],
)

mainGraph = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3(
                                    "Zimbabwe Industry Balance of Trader, Economic Indicator"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="chart-type-filter",
                                                value="mixed",
                                                options=[
                                                    {
                                                        "value": "line",
                                                        "label": "line chart",
                                                    },
                                                    {
                                                        "value": "bar",
                                                        "label": "bar chart",
                                                    },
                                                    {
                                                        "value": "mixed",
                                                        "label": "bar & line chart",
                                                    },
                                                ],
                                                clearable=False,
                                                placeholder="choose chart type",
                                            ),
                                            width={
                                                "size": 4,
                                            },
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    dbc.ButtonGroup(
                                                        [
                                                            dbc.Button(
                                                                "Primary",
                                                                id="primary-opt",
                                                                color="primary",
                                                                className="mr-1",
                                                                n_clicks=0,
                                                                size="lg",
                                                            ),
                                                            dbc.Button(
                                                                "Secondary",
                                                                n_clicks=0,
                                                                id="secondary-opt",
                                                                color="secondary",
                                                                className="mr-1",
                                                                size="lg",
                                                            ),
                                                        ],
                                                        size="lg",
                                                        className="mr-1",
                                                    ),
                                                ]
                                            ),
                                            width={
                                                "size": 4,
                                            },
                                        ),
                                    ],
                                    justify="between",
                                ),
                                dcc.Graph(
                                    id="btei-graph",
                                    figure={
                                        "data": [
                                            {
                                                "x": dfAit[6],
                                                "y": dfAit[7],
                                                "type": "bar",
                                                "name": "Imports",
                                            },
                                            {
                                                "x": dfAit[6],
                                                "y": dfAit[8],
                                                "type": "bar",
                                                "name": "Exports",
                                            },
                                            {
                                                "x": dfAit[6],
                                                "y": dfAit[9],
                                                "name": "Trade Surplus",
                                                "type": "lines",  # toggle between 'lines' and 'bar'
                                                "color": "grey",
                                            },
                                        ]
                                    },
                                ),
                            ],
                        ),
                    ),
                ),
            ]
        ),
    ]
)

app.layout = html.Div(
    children=[
        jumbtronHeader,
        html.Div(
            [
                summaryCard,
            ],
            id="eco-graph-data",
        ),
        html.Div(
            [mainGraph],
            id="ait-graph-data",
        ),
    ],
)

# callback definition
@app.callback(
    Output("eco-graph-data", "children"),
    [
        Input("upload-ei-data", "contents"),
        Input("upload-ei-data", "filename"),
    ],
)
def update_ei_based_layout(contents, filename):
    global dfEco

    if contents and filename:
        dfEco = parse_data(filename, contents)

    eiLayout = summaryCard

    return eiLayout


@app.callback(
    Output("ait-graph-data", "children"),
    [
        Input("upload-ait-data", "contents"),
        Input("upload-ait-data", "filename"),
    ],
)
def update_ait_based_layout(contents, filename):
    global dfAit

    if contents and filename:
        dfAit = parse_data(filename, contents)

    aitLayout = mainGraph

    return aitLayout


@app.callback(
    Output("summary-year-value", "children"),
    Output("budget-deficit", "children"),
    Output("bd-perc-change", "children"),
    Output("imports", "children"),
    Output("imports-perc-change", "children"),
    Output("exports", "children"),
    Output("exports-perc-change", "children"),
    Output("net-imports", "children"),
    Output("net-imports-perc-change", "children"),
    Output("inflation-rate", "children"),
    Output("ira-perc-change", "children"),
    Output("growth-rate", "children"),
    Output("rgr-perc-change", "children"),
    Output("gvt-expenditure", "children"),
    Output("getgdp-perc-change", "children"),
    Output("private-inv", "children"),
    Output("pigdp-imports-perc-change", "children"),
    Input("summary-year-filter", "value"),
)
def update_summary_year_div(summary_year):
    return parse_summary(html, list(dfEco.columns.values), summary_year, dfEco)


@app.callback(
    Output("primary-opt", "color"),
    Output("secondary-opt", "color"),
    Output("btei-graph", "figure"),
    Input("primary-opt", "n_clicks"),
    Input("secondary-opt", "n_clicks"),
    Input("chart-type-filter", "value"),
)
def update_main_chart_btn_color(primary_btn, secondary_btn, chart_type):
    # return btn color change + chart type + indicated data-source
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    pri = "primary"
    sec = "secondary"
    barChart = "bar"
    assumedLineChart = "lines"

    if chart_type == "bar":
        assumedLineChart = "bar"

    elif chart_type == "line":
        barChart = "lines"

    if "primary-opt" in changed_id:
        pri = "primary"
        sec = "secondary"

    elif "secondary-opt" in changed_id:
        pri = "secondary"
        sec = "primary"

    if pri == "secondary":
        figureUpdate = {
            "data": [
                {"x": dfAit[0], "y": dfAit[1], "type": barChart, "name": "Imports"},
                {"x": dfAit[0], "y": dfAit[2], "type": barChart, "name": "Exports"},
                {
                    "x": dfAit[0],
                    "y": dfAit[3],
                    "name": "Trade Deficit",
                    "type": assumedLineChart,  # toggle between 'lines' and 'bar'
                    "color": "grey",
                },
            ]
        }

    else:
        figureUpdate = {
            "data": [
                {
                    "x": dfAit[6],
                    "y": dfAit[7],
                    "type": barChart,
                    "name": "Imports",
                },
                {
                    "x": dfAit[6],
                    "y": dfAit[8],
                    "type": barChart,
                    "name": "Exports",
                },
                {
                    "x": dfAit[6],
                    "y": dfAit[9],
                    "name": "Trade Surplus",
                    "type": assumedLineChart,  # toggle between 'lines' and 'bar'
                    "color": "grey",
                },
            ]
        }

    return pri, sec, figureUpdate

if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
