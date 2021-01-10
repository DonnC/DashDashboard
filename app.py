'''
@author: <https://github.com/DonnC>
@created: 08 Jan 2021
@project: dash dashboard
'''

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash

from utility import parse_data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# load static data
# annual international trade stats
dfAit = parse_data(filename='data/ait.csv', isFileOnly=True)

# economic indicators
dfEco = parse_data(filename='data/eco-data.csv', isFileOnly=True)

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

jumbtronHeader = dbc.Jumbotron([
    html.H1("Dashboard", className="display-6"),
    html.P(
        "Analyse and visualize trade deficit GDP and inflation. "
        "All intepreted from 2 variable exports and imports. "
        "from two industries: Primary Industry and Secondary Industry",
        className="lead", ),
    dbc.Row([
        dbc.Button(uploadAit, size="md", className="mr-1", ),
        dbc.Button(uploadEind, size="md", className="mr-1", ),
    ],
        justify="end",
    ),
],
)


def summaryYearItems(yearList):
    items = []

    for year in yearList:
        items.append(
            {
                "value": f"{year}",
                "label": f"{year}",
            }
        )

    return items


def summaryCard(title, valueID, percChangeID):
    '''
    create a summary card
    :param title: title of card tile
    :param valueID: id of the value being dynamically changed
    :param percChangeID: id of the percentage change
    :return: dbc.Card component
    '''

    summaryCard = dbc.Card(
        [
            dbc.CardBody([
                html.H3(title, style={'color': 'grey'}),
                #html.H1("2382", id=valueID, style={'size': 40}),
                html.Div(id=valueID),
                html.Div(id=percChangeID),
                #html.H5("3.23%", id=percChangeID, style={'color': 'grey', 'size': 25}),
                html.H6('Since previous year', style={'color': 'grey'})
            ])
        ])
    return summaryCard


def getFirstRowSummaryCards():
    cards = []

    budgetDeficit = summaryCard(title="BUDGET DEFICIT", valueID="budget-deficit", percChangeID="bd-perc-change")
    imports_ = summaryCard(title="IMPORTS", valueID="imports", percChangeID="imports-perc-change")
    exports_ = summaryCard(title="EXPORTS", valueID="exports", percChangeID="exports-perc-change")
    netImports = summaryCard(title="NET IMPORTS", valueID="net-imports", percChangeID="net-imports-perc-change")

    cards.append(budgetDeficit)
    cards.append(imports_)
    cards.append(exports_)
    cards.append(netImports)

    return cards


def getSecondRowSummaryCards():
    cards = []

    inflationRatesAnn = summaryCard(title="INFLATION RATE ANNUAL CHANGE", valueID="inflation-rate",
                                    percChangeID="ira-perc-change")
    realGroRate = summaryCard(title="REAL GROWTH RATE / ANNUM", valueID="growth-rate", percChangeID="rgr-perc-change")
    gvtExpToGdp = summaryCard(title="GVT EXPENDITURE-GDP RATIO", valueID="gvt-expenditure",
                              percChangeID="getgdp-perc-change")
    privInvGdp = summaryCard(title="PVT INVESTMENT / GDP", valueID="private-inv",
                             percChangeID="pigdp-imports-perc-change")

    cards.append(inflationRatesAnn)
    cards.append(realGroRate)
    cards.append(gvtExpToGdp)
    cards.append(privInvGdp)

    return cards


summaryYears = [2008, 2009, 2010, 1999, 2000]

summaryCard = html.Div(
    [
        dbc.Card([
            dbc.CardHeader([
                dbc.Row(
                    [
                        dbc.Col(html.Div("Summary for Year:", className="card-text", ), width=4),
                        dbc.Col(html.Div(id="summary-year-value"), width=4),
                    ],
                    justify="start",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="summary-year-filter",
                        value=summaryYears[-1],
                        options=summaryYearItems(summaryYears),
                        clearable=False,
                        placeholder='Select Year',
                    ),
                    width={'size': 4}
                ),
            ],
            ),
            dbc.CardBody([
                dbc.Row([
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
                    className="mb-4", ),
                dbc.Row([
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
                    className="mb-4", ),
            ], ),

        ],

        ),
    ],
)

app.layout = html.Div(
    children=[
        jumbtronHeader,
        summaryCard,
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("Zimbabwe Industry Balance of Trader, Economic Indicator"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='chart-type-filter',
                                            value='mixed',
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
                                                }
                                            ],
                                            clearable=False,
                                            placeholder='choose chart type',
                                        ),
                                        width={"size": 4, },
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
                                                            size="lg"),
                                                        dbc.Button(
                                                            "Secondary",
                                                            n_clicks=0,
                                                            id="secondary-opt",
                                                            color="secondary",
                                                            className="mr-1",
                                                            size="lg"),
                                                    ],
                                                    size="lg",
                                                    className="mr-1",
                                                ),
                                            ]

                                        ),
                                        width={"size": 4, },
                                    ),
                                ],
                                justify="between",
                            ),
                            dcc.Graph(
                                id="btei-graph",
                                figure={
                                    'data': [
                                        {'x': dfAit[6], 'y': dfAit[7], 'type': 'bar', 'name': 'Imports'},
                                        {'x': dfAit[6], 'y': dfAit[8], 'type': 'bar', 'name': 'Exports'},
                                        {
                                            "x": dfAit[6],
                                            "y": dfAit[9],
                                            'name': 'Trade Surplus',
                                            "type": "lines",  # toggle between 'lines' and 'bar'
                                            'color': 'grey',
                                        },
                                    ]
                                }
                            ),
                        ],
                    ),
                ),

            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Economic Indicators figures"),
                        dcc.Graph(
                            id="eind-graph",
                            figure={
                                "data": [
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[2],
                                        "type": "lines",
                                        'name': 'GDP@MP',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[3],
                                        "type": "lines",
                                        'name': 'Gvt Debt',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[4],
                                        "type": "lines",
                                        'name': 'Revenue & Grants',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[5],
                                        "type": "lines",
                                        'name': 'Gvt Expenditure',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[6],
                                        "type": "lines",
                                        'name': 'Budget deficit',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[7],
                                        "type": "lines",
                                        'name': 'Gen Gvt(GFCF)',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[9],
                                        "type": "bar",
                                        'name': 'Total GFCF',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[10],
                                        "type": "bar",
                                        'name': 'Pvt Inv (GFCF)',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[19],
                                        "type": "bar",
                                        'name': 'Money Supply (millions)',
                                    },
                                    {
                                        "x": dfEco[0],
                                        "y": dfEco[22],
                                        "type": "bar",
                                        'name': 'Population(ml)',
                                    },
                                ],
                            },
                        ),
                    ]),
                ),

                width=4,
            ),
        ]),
    ],
)

# callback definition
@app.callback(
    Output('summary-year-value', 'children'),

    Input('summary-year-filter', 'value'))
def update_summary_year_div(summary_year):
    return f"   {summary_year}"


@app.callback(Output('primary-opt', 'color'),
              Output('secondary-opt', 'color'),
              Output('btei-graph', 'figure'),
              Input('primary-opt', 'n_clicks'),
              Input('secondary-opt', 'n_clicks'),
              Input('chart-type-filter', 'value'))
def update_main_chart_btn_color(primary_btn, secondary_btn, chart_type):
    # return btn color change + chart type + indicated data-source
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    pri = 'primary'
    sec = 'secondary'
    barChart = 'bar'
    assumedLineChart = 'lines'

    if chart_type == 'bar':
        assumedLineChart = 'bar'

    elif chart_type == 'line':
        barChart = 'lines'

    if 'primary-opt' in changed_id:
        pri = 'primary'
        sec = 'secondary'
        msg = 'Primary: Button 1 was most recently clicked'

    elif 'secondary-opt' in changed_id:
        pri = 'secondary'
        sec = 'primary'
        msg = 'Secondary: Button 2 was most recently clicked'

    else:
        msg = 'None of the buttons have been clicked yet'

    if pri == 'secondary':
        figureUpdate = {
            'data': [
                {'x': dfAit[0], 'y': dfAit[1], 'type': barChart, 'name': 'Imports'},
                {'x': dfAit[0], 'y': dfAit[2], 'type': barChart, 'name': 'Exports'},
                {
                    "x": dfAit[0],
                    "y": dfAit[3],
                    'name': 'Trade Deficit',
                    "type": assumedLineChart,  # toggle between 'lines' and 'bar'
                    'color': 'grey',
                },
            ]
        }

    else:
        figureUpdate = {
            'data': [
                {'x': dfAit[6], 'y': dfAit[7], 'type': barChart, 'name': 'Imports'},
                {'x': dfAit[6], 'y': dfAit[8], 'type': barChart, 'name': 'Exports'},
                {
                    "x": dfAit[6],
                    "y": dfAit[9],
                    'name': 'Trade Surplus',
                    "type": assumedLineChart,  # toggle between 'lines' and 'bar'
                    'color': 'grey',
                },
            ]
        }

    return pri, sec, figureUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
