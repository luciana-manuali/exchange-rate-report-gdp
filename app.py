import pathlib
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Output, Input
import datetime as dt
import pandas_datareader.data as web
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

wire_cost = ((exchange_rate['MEP']/ exchange_rate['CCL'])-1)*-100

real_exchange_rate = pd.read_excel('http://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/ITCRMSerie.xls', header = 1, index_col = 0,
              usecols = 'A,B,C,F').dropna().iloc[800:]
for i, n in zip(real_exchange_rate.index, range(len(real_exchange_rate.index))):
    real_exchange_rate = real_exchange_rate.rename(index={i: xlrd.xldate_as_datetime(i, 0)})

new_index = pd.date_range(start="2014-05-27",end="2022-12-12")
exchange_rate_ = exchange_rate[~exchange_rate.index.duplicated()]
exchange_rate_ = exchange_rate_.reindex(new_index, method='bfill')

arg_ipc = pd.read_excel('https://ucema.edu.ar/_externo/cea_vce/table_download.php?s=66', engine='openpyxl')
arg_ipc = arg_ipc[['Fecha','Nivel']]
arg_ipc.rename(columns = {'Fecha':'Date', 'Nivel':'IPC'}, inplace = True)
arg_ipc = arg_ipc.set_index('Date')
arg_ipc = arg_ipc.sort_index()
arg_ipc.index = arg_ipc.index.strftime('%Y-%m-%d')
arg_ipc.index = pd.to_datetime(arg_ipc.index)
arg_ipc = arg_ipc[~arg_ipc.index.duplicated()]

sdt = dt.datetime(1970, 1, 1)
usa_cpi = web.DataReader("CPIAUCNS", "fred", sdt)
usa_cpi.columns = ['CPI USA']
usa_cpi = usa_cpi.rename_axis('Date')
usa_cpi = usa_cpi[~usa_cpi.index.duplicated()]

implicit_exchange_rate = pd.DataFrame()
implicit_exchange_rate['Official'] = exchange_rate_['Official']
implicit_exchange_rate['MEP'] = exchange_rate_['MEP']
implicit_exchange_rate['CCL'] = exchange_rate_['CCL']
implicit_exchange_rate['CPI USA'] = usa_cpi['CPI USA'].loc[usa_cpi['CPI USA'].index[0]:]/usa_cpi['CPI USA'].loc[usa_cpi['CPI USA'].index[0]]*100
implicit_exchange_rate['CPI ARG'] = arg_ipc.loc[arg_ipc.index[0]:]/arg_ipc.loc[arg_ipc.index[0]]*100
implicit_exchange_rate = implicit_exchange_rate.dropna()
implicit_exchange_rate['Implicit Official'] = implicit_exchange_rate['Official']*(implicit_exchange_rate['CPI USA']/implicit_exchange_rate['CPI ARG'])*(implicit_exchange_rate['CPI ARG'].iloc[-1]/implicit_exchange_rate['CPI USA'].iloc[-1])
implicit_exchange_rate['Implicit MEP'] = implicit_exchange_rate['MEP']*(implicit_exchange_rate['CPI USA']/implicit_exchange_rate['CPI ARG'])*(implicit_exchange_rate['CPI ARG'].iloc[-1]/implicit_exchange_rate['CPI USA'].iloc[-1])
implicit_exchange_rate['Implicit CCL'] = implicit_exchange_rate['CCL']*(implicit_exchange_rate['CPI USA']/implicit_exchange_rate['CPI ARG'])*(implicit_exchange_rate['CPI ARG'].iloc[-1]/implicit_exchange_rate['CPI USA'].iloc[-1])

# Colors

color_1 = '#641E16'

colors = ['#000000','#E34234','#C4A484',
          '#708090','#D3D3D3','#36454F','#7C3030','#C04000','#C19A6B','#C41E3A','#CC5500',
          '#A42A04','#E3735E','#818589','#E5E4E2','#EE4B2B','#EADDCA',
          '#FF0000','#C0C0C0']

colors_ = ['#E34234','#C4A484',
          '#708090','#D3D3D3','#36454F','#7C3030','#C04000','#C19A6B','#C41E3A','#CC5500',
          '#A42A04','#E3735E','#818589','#E5E4E2','#EE4B2B','#EADDCA',
          '#FF0000','#C0C0C0']

# Layout

app = dash.Dash(__name__)
app.title = "Exchange Rate Report Grupo del Plata S.A."
server = app.server

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
                                    id="date-range",
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
                                    id="date-range2",
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
        # Page 4
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Strong(
                                            "Figure 3: Wire Cost",
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
                                    id="date-range3",
                                    min_date_allowed=wire_cost.index.min().date(),
                                    max_date_allowed=wire_cost.index.max().date(),
                                    start_date=wire_cost.index.min().date(),
                                    end_date=wire_cost.index.max().date(),
                                    updatemode='singledate',
                                )
                                ,
                                dcc.Graph(id="wire-cost",
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
                                        html.H6("3"),
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
                                    id="date-range4",
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
        # Page 6
        #html.Div(
        #    [
        #        html.Div(
        #            [
        #                html.Div(
        #                    [
        #                        html.Div(
        #                            [
        #                                html.Strong(
        #                                    "Figure 5: Implicit Exchange Rates",
        #                                ),
        #                            ],
        #                            style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'center',
        #                                   'color': color_1},
        #                        ),
        #                        html.Div(
        #                            [
        #                                html.Img(
        #                                    src=app.get_asset_url(
        #                                        "logo_.png"
        #                                    ),
        #                                    style={'opacity': '0.2'},
        #                                    className='page-1a',
        #                                ),
        #                            ],
        #                            style={'width': '10%', 'display': 'inline-block', 'vertical-align': 'center',
        #                                   'text-align': 'right', 'color': 'black'},
        #                        ),
        #                    ],
        #                    className="row",
        #                ),
        #                html.Div(
        #                    [
        #                        html.P(
        #                            "",
        #                        ),
        #                        dcc.DatePickerRange(
        #                            id="date-range5",
        #                            min_date_allowed=implicit_exchange_rate.index.min().date(),
        #                            max_date_allowed=implicit_exchange_rate.index.max().date(),
        #                            start_date=implicit_exchange_rate.index.min().date(),
        #                            end_date=implicit_exchange_rate.index.max().date(),
        #                            updatemode='singledate',
        #                        )
        #                        ,
        #                        dcc.Graph(id="implicit-exchange-rate",
        #                                  config={"displayModeBar": False},
        #                                  ),
        #                    ],
        #                    className="thirdPage first row",
        #                ),
        #                html.Div(
        #                    [
        #                        html.Div(
        #                            [
        #                                html.H1("SPACE"),
        #                            ],
        #                            style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'center',
        #                                   'color': 'white'},
        #                        ),
        #                        html.Div(
        #                            [
        #                                html.H6("5"),
        #                            ],
        #                            style={'width': '5%', 'display': 'inline-block', 'vertical-align': 'center',
        #                                   'text-align': 'right', 'color': 'black'},
        #                        ),
        #                    ],
        #                    className="row",
        #                ),
        #            ],
        #            className="subpage",
        #        )
        #    ],
        #    className="page",
        #),

    ]
)


@app.callback(
    Output("exchange-rate", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"), ],
)
def historica_perf(start_date, end_date):
    mask = (exchange_rate.index >= pd.to_datetime(start_date)) & \
           (exchange_rate.index <= pd.to_datetime(end_date))

    filtered_data = exchange_rate.iloc[mask]

    fig1 = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig1.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig1.update_layout(
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

    return fig1

@app.callback(
    Output("spread", "figure"),
    [
        Input("date-range2", "start_date"),
        Input("date-range2", "end_date"), ],
)
def historica_perf(start_date, end_date):
    mask = (spread.index >= pd.to_datetime(start_date)) & \
           (spread.index <= pd.to_datetime(end_date))

    filtered_data = spread.iloc[mask]

    fig2 = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig2.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig2.update_layout(
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

    return fig2

@app.callback(
    Output("wire-cost", "figure"),
    [
        Input("date-range3", "start_date"),
        Input("date-range3", "end_date"), ],
)
def historica_perf(start_date, end_date):
    mask = (wire_cost.index >= pd.to_datetime(start_date)) & \
           (wire_cost.index <= pd.to_datetime(end_date))

    filtered_data = wire_cost.iloc[mask]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=filtered_data.index,
                              y=filtered_data,
                              mode='lines',
                              connectgaps=True,
                              name = "Wire Cost",
                              line=dict(
                                  color = colors[1],
                              ),
                              ),
                   )
    fig3.update_layout(
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
            title= 'Wire Cost (%)',
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

    return fig3

@app.callback(
    Output("real-exchange-rate", "figure"),
    [
        Input("date-range4", "start_date"),
        Input("date-range4", "end_date"), ],
)
def historica_perf(start_date, end_date):
    mask = (real_exchange_rate.index >= pd.to_datetime(start_date)) & \
           (real_exchange_rate.index <= pd.to_datetime(end_date))

    filtered_data = real_exchange_rate.iloc[mask]

    fig4 = go.Figure()
    for i, color in zip(filtered_data.columns, colors):
        fig4.add_trace(go.Scatter(x=filtered_data[i].index,
                                  y=filtered_data[i],
                                  mode='lines',
                                  connectgaps=True,
                                  name=i,
                                  line=dict(
                                      color=color
                                  )
                                  )
                       )
    fig4.update_layout(
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

    return fig4

#@app.callback(
#    Output("implicit-exchange-rate", "figure"),
#    [
#        Input("date-range5", "start_date"),
#        Input("date-range5", "end_date"), ],
#)
#def historica_perf(start_date, end_date):
#    mask = (implicit_exchange_rate.index >= pd.to_datetime(start_date)) & \
#           (implicit_exchange_rate.index <= pd.to_datetime(end_date))
#
#    filtered_data = implicit_exchange_rate.drop(['CPI USA','CPI ARG'], axis=1).iloc[mask]

#    fig5 = go.Figure()
#    for i, color in zip(filtered_data.columns, colors):
#        fig5.add_trace(go.Scatter(x=filtered_data[i].index,
#                                  y=filtered_data[i],
#                                  mode='lines',
#                                  connectgaps=True,
#                                  name=i,
#                                  line=dict(
#                                      color=color
#                                  )
#                                  )
#                       )
#    fig5.update_layout(
#        xaxis=dict(
#            showgrid=True,
#            showline=True,
#            zeroline=True,
#            gridcolor="lightgray",
#            zerolinecolor="lightgray",
#            showticklabels=True,
#            tickformat="%m-%Y",
#            linecolor="lightgray",
#            tickcolor="lightgray",
#            tickangle=-90,
#            ticks='outside',
#            type='date',
#            tickfont=dict(
#                family='Arial',
#                size=9,
#            ),
#        ),
#        yaxis=dict(
#            showgrid=True,
#            showline=True,
#            showticklabels=True,
#            zeroline=True,
#            zerolinecolor="lightgray",
#            gridcolor="lightgray",
#            linecolor="lightgray",
#            tickcolor="lightgray",
#            titlefont=dict(
#                family='Arial',
#                size=9,
#            ),
#            tickfont=dict(
#                family='Arial',
#                size=9,
#            ),
#        ),
#        margin=dict(
#            r=10,
#            t=5,
#            b=0,
#            l=40,
#            pad=2,
#        ),
#        legend=dict(
#            yanchor="top",
#            y=1.3,
#            xanchor="center",
#            x=0.55,
#            orientation="h",
#            font=dict(
#                family='Arial',
#                size=9,
#            ),
#        ),
#        height=450,
#        showlegend=True,
#        plot_bgcolor='rgba(0,0,0,0)',
#    )

#    return fig5

if __name__ == "__main__":
    app.run_server(debug=True)
