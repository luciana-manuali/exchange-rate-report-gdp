import pathlib
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Output, Input
import datetime as dt
import xlrd

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()

# Data
exchange_rate = pd.read_excel(DATA_PATH.joinpath("Exchange Rate.xlsm"), engine='openpyxl')

# Variables

title = 'Exchange Rate Report'
now = dt.datetime.now()

exchange_rate = exchange_rate.round(2)
exchange_rate.set_index(['Date'],inplace=True)
exchange_rate.index = pd.to_datetime(exchange_rate.index)

spread = pd.DataFrame()
spread['MEP Spread'] = ((exchange_rate['MEP']/exchange_rate['Official'])-1)*100
spread['CCL Spread'] = ((exchange_rate['CCL']/exchange_rate['Official'])-1)*100

real_exchange_rate = pd.read_excel('http://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/ITCRMSerie.xls', header = 1, index_col = 0,
              usecols = 'A,B,C,F').dropna().iloc[800:]
for i, n in zip(real_exchange_rate.index, range(len(real_exchange_rate.index))):
    real_exchange_rate = real_exchange_rate.rename(index={i: xlrd.xldate_as_datetime(i, 0)})

# Colors

color_1 = '#641E16'

colors = ['#000000','#E34234','#C4A484',
          '#708090','#D3D3D3','#36454F','#7C3030','#C04000','#C19A6B','#C41E3A','#CC5500',
          '#A42A04','#E3735E','#818589','#E5E4E2','#EE4B2B','#EADDCA',
          '#FF0000','#C0C0C0']

# Layout

app = dash.Dash(__name__)
server = app.server

app.title = "Exchange Rate Report Grupo del Plata S.A."

app.layout = html.Div(
    children=[
        #Page 1
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                    ],
                                    style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'middle'},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H1("SPACE"),
                                            ],
                                            style={'display': 'inline-block', 'vertical-align': 'center',
                                                   'color': 'white'},
                                        ),
                                        html.Div(
                                            [
                                                html.H1(title),
                                                html.P("SPACE", style={'color': 'white'}),
                                                html.H3(now.strftime("%m-%d-%Y")),
                                                html.H2("Grupo del Plata S.A."),
                                                html.Img(
                                                    src=app.get_asset_url(
                                                        "big_logo.png"
                                                    ),
                                                    className='page-1a',
                                                ),
                                                ],
                                        ),
                                        html.Div(
                                            [
                                                html.H6("SPACE"),
                                            ],
                                            style={'display': 'inline-block', 'vertical-align': 'center',
                                                   'color': 'white'},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.P(""),
                                                        html.H6("Ph.D. Jonatan Saul", className="page-1h"),
                                                        html.P(""),
                                                        html.P("Research and Strategy"),
                                                        html.P("jsaul@gdelplata.com"),
                                                        ],
                                                    style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'center'},
                                                ),
                                                html.Div(
                                                    [
                                                        html.P(""),
                                                        html.H6("Lic. Luciana Manuali", className="page-1h"),
                                                        html.P(""),
                                                        html.P("Research"),
                                                        html.P("amanuali@gdelplata.com"),
                                                        ],
                                                    style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'center'},
                                                ),
                                                html.Div(
                                                    [
                                                        html.P(""),
                                                        html.H6("Lic. Mateo Riba", className="page-1h"),
                                                        html.P(""),
                                                        html.P("Trading"),
                                                        html.P("mriba@gdelplata.com")
                                                        ],
                                                    style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'center'},
                                                ),
                                                html.Div(
                                                    [
                                                        html.P(""),
                                                        html.H6("Santiago Ahumada", className="page-1h"),
                                                        html.P(""),
                                                        html.P("Trading"),
                                                        html.P("sahumada@gdelplata.com")
                                                    ],
                                                    style={'width': '25%', 'display': 'inline-block',
                                                           'vertical-align': 'center'},
                                                ),
                                            ],
                                            className="row",
                                        ),
                                    ],
                                    style={'width': '70%', 'display': 'inline-block', 'text-align': 'center', 'horizontal-align': 'middle'},
                                ),
                                html.Div(
                                    [
                                    ],
                                    style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'middle'},
                                ),
                            ],
                            className="row"
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),
        # Page 2
        html.Div(
            children=[
                html.Div(
                    [
                        html.Div(
                           [
                                html.Div(
                                    [
                                        html.Strong(
                                            "Figure 1: Exchange Rates",
                                        ),
                                    ],
                                    style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'center', 'color': color_1},
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            src=app.get_asset_url(
                                                "logo_.png"
                                            ),
                                            style={'opacity': '0.2'},
                                            className='page-1a',
                                        ),
                                    ],
                                    style={'width': '10%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'text-align': 'right', 'color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            [
                                html.P(
                                    "",
                                ),
                                dcc.DatePickerRange(
                                    id="date-range-exchange-rate",
                                    min_date_allowed=exchange_rate.index.min().date(),
                                    max_date_allowed=exchange_rate.index.max().date(),
                                    start_date=exchange_rate.index.min().date(),
                                    end_date=exchange_rate.index.max().date(),
                                    updatemode='singledate',
                                )
                                ,
                                dcc.Graph(id="exchange-rate",
                                          config={"displayModeBar": False},
                                          ),
                            ],
                            className="thirdPage first row",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H1("SPACE"),
                                    ],
                                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'center','color': 'white'},
                                ),
                                html.Div(
                                    [
                                        html.H6("1"),
                                    ],
                                    style={'width': '5%','display': 'inline-block', 'vertical-align': 'center', 'text-align': 'right','color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),
        # Page 3
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Strong(
                                            "Figure 2: MEP Spread and CCL Spread",
                                        ),
                                    ],
                                    style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'color': color_1},
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            src=app.get_asset_url(
                                                "logo_.png"
                                            ),
                                            style={'opacity': '0.2'},
                                            className='page-1a',
                                        ),
                                    ],
                                    style={'width': '10%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'text-align': 'right', 'color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            [
                                html.P(
                                    "",
                                ),
                                dcc.DatePickerRange(
                                    id="date-range-spread",
                                    min_date_allowed=spread.index.min().date(),
                                    max_date_allowed=spread.index.max().date(),
                                    start_date=spread.index.min().date(),
                                    end_date=spread.index.max().date(),
                                    updatemode='singledate',
                                )
                                ,
                                dcc.Graph(id="spread",
                                          config={"displayModeBar": False},
                                          ),
                            ],
                            className="thirdPage first row",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H1("SPACE"),
                                    ],
                                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'color': 'white'},
                                ),
                                html.Div(
                                    [
                                        html.H6("2"),
                                    ],
                                    style={'width': '5%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'text-align': 'right', 'color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),
        # Page 5
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Strong(
                                            "Figure 4: Real Multilateral Exchange Rate Indices ",
                                        ),
                                    ],
                                    style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'color': color_1},
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            src=app.get_asset_url(
                                                "logo_.png"
                                            ),
                                            style={'opacity': '0.2'},
                                            className='page-1a',
                                        ),
                                    ],
                                    style={'width': '10%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'text-align': 'right', 'color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            [
                                html.P(
                                    "",
                                ),
                                dcc.DatePickerRange(
                                    id="date-range-real-exchange-rate",
                                    min_date_allowed=real_exchange_rate.index.min().date(),
                                    max_date_allowed=real_exchange_rate.index.max().date(),
                                    start_date=real_exchange_rate.index.min().date(),
                                    end_date=real_exchange_rate.index.max().date(),
                                    updatemode='singledate',
                                )
                                ,
                                dcc.Graph(id="real-exchange-rate",
                                          config={"displayModeBar": False},
                                          ),
                            ],
                            className="thirdPage first row",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H1("SPACE"),
                                    ],
                                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'color': 'white'},
                                ),
                                html.Div(
                                    [
                                        html.H6("4"),
                                    ],
                                    style={'width': '5%', 'display': 'inline-block', 'vertical-align': 'center',
                                           'text-align': 'right', 'color': 'black'},
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),
    ]
)


@app.callback(
    Output("exchange-rate", "figure"),
    [
        Input("date-range-exchange-rate", "start_date"),
        Input("date-range-exchange-rate", "end_date"), ],
)
def historical_performance(start_date, end_date):
    mask = (exchange_rate.index >= pd.to_datetime(start_date)) & \
           (exchange_rate.index <= pd.to_datetime(end_date))

    filtered_data = exchange_rate.iloc[mask]

    fig_exchange_rate = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig_exchange_rate.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig_exchange_rate.update_layout(
        xaxis=dict(
            showgrid=True,
            showline=True,
            zeroline=True,
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            showticklabels=True,
            tickformat="%m-%Y",
            linecolor="lightgray",
            tickcolor="lightgray",
            tickangle=-90,
            ticks='outside',
            type='date',
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror=True,
        ),
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=True,
            zerolinecolor="lightgray",
            gridcolor="lightgray",
            linecolor="lightgray",
            tickcolor="lightgray",
            titlefont=dict(
                family='Arial',
                size=12,
            ),
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror= True,
            side='right',
        ),
        margin=dict(
            r=10,
            t=5,
            b=0,
            l=40,
            pad=2,
        ),
        legend=dict(
            yanchor="top",
            y=1.3,
            xanchor="center",
            x=0.55,
            orientation="h",
            font=dict(
                family='Arial',
                size=12,
            ),
        ),
        height=450,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig_exchange_rate

@app.callback(
    Output("spread", "figure"),
    [
        Input("date-range-spread", "start_date"),
        Input("date-range-spread", "end_date"), ],
)
def spread_calculation(start_date, end_date):
    mask = (spread.index >= pd.to_datetime(start_date)) & \
           (spread.index <= pd.to_datetime(end_date))

    filtered_data = spread.iloc[mask]

    fig_spread = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig_spread.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig_spread.update_layout(
        xaxis=dict(
            showgrid=True,
            showline=True,
            zeroline=True,
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            showticklabels=True,
            tickformat="%m-%Y",
            linecolor="lightgray",
            tickcolor="lightgray",
            tickangle=-90,
            ticks='outside',
            type='date',
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror=True,
        ),
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=True,
            zerolinecolor="lightgray",
            gridcolor="lightgray",
            linecolor="lightgray",
            tickcolor="lightgray",
            titlefont=dict(
                family='Arial',
                size=12,
            ),
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror=True,
            side='right',
        ),
        margin=dict(
            r=10,
            t=5,
            b=0,
            l=40,
            pad=2,
        ),
        legend=dict(
            yanchor="top",
            y=1.3,
            xanchor="center",
            x=0.55,
            orientation="h",
            font=dict(
                family='Arial',
                size=12,
            ),
        ),
        height=450,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig_spread

@app.callback(
    Output("real-exchange-rate", "figure"),
    [
        Input("date-range-real-exchange-rate", "start_date"),
        Input("date-range-real-exchange-rate", "end_date"), ],
)
def real_exchange_rate_calculation(start_date, end_date):
    mask = (real_exchange_rate.index >= pd.to_datetime(start_date)) & \
           (real_exchange_rate.index <= pd.to_datetime(end_date))

    filtered_data = real_exchange_rate.iloc[mask]

    fig_real_exchange_rate = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig_real_exchange_rate.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig_real_exchange_rate.update_layout(
        xaxis=dict(
            showgrid=True,
            showline=True,
            zeroline=True,
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            showticklabels=True,
            tickformat="%m-%Y",
            linecolor="lightgray",
            tickcolor="lightgray",
            tickangle=-90,
            ticks='outside',
            type='date',
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror=True,
        ),
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=True,
            zerolinecolor="lightgray",
            gridcolor="lightgray",
            linecolor="lightgray",
            tickcolor="lightgray",
            titlefont=dict(
                family='Arial',
                size=12,
            ),
            tickfont=dict(
                family='Arial',
                size=12,
            ),
            mirror=True,
            side='right',
        ),
        margin=dict(
            r=10,
            t=5,
            b=0,
            l=40,
            pad=2,
        ),
        legend=dict(
            yanchor="top",
            y=1.3,
            xanchor="center",
            x=0.55,
            orientation="h",
            font=dict(
                family='Arial',
                size=12,
            ),
        ),
        height=450,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig_real_exchange_rate

if __name__ == "__main__":
    app.run_server(debug=True)
