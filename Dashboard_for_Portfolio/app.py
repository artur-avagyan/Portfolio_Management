import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from mni import create_mesh_data, default_colorscale
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)


app = dash.Dash(
    __name__,
    # meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Portfolio Managment Dashboard"

# server = app.server

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/artur-avagyan/Portfolio_Management",
)

default_colorscale_index = [ea[1] for ea in default_colorscale]

axis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    "plot_bgcolor": "#141414",
    "paper_bgcolor": "#141414",
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectratio": {"x": 1, "y": 1.2, "z": 1},
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

plot_layout_2 = {
    # "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    # "showlegend": False,
    "plot_bgcolor": "#141414",
    "paper_bgcolor": "#141414",
    "autosize": True,
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
    },
}

options_stocks_checklist=[
        {'label': '(AMZN) Amazon.com, Inc.', 'value': 'AMZN'},
        {'label': '(C) Citigroup Inc.', 'value': 'C'},
        {'label': '(AAPL) Apple Inc.', 'value': 'AAPL'},
        {'label': '(IBM) Intern. Bus. Mach. Corp.', 'value': 'IBM'},
        {'label': '(CSCO) Cisco Systems, Inc.', 'value': 'CSCO'},
        {'label': '(NVDA) NVIDIA Corporation', 'value': 'NVDA'},
        {'label': '(MSFT) Microsoft Corporation', 'value': 'MSFT'},
        {'label': '(TM) Toyota Motor Corporation', 'value': 'TM'},
        {'label': '(CVX) Chevron Corporation', 'value': 'CVX'},
        {'label': '(GOOG) Alphabet Inc.', 'value': 'GOOG'},
        {'label': '(FB) Meta Platforms, Inc.', 'value': 'FB'},
        {'label': '(TSLA) Tesla, Inc.', 'value': 'TSLA'},
        {'label': '(JPM) JPMorgan Chase & Co.', 'value': 'JPM'},
        {'label': '(JNJ) Johnson & Johnson', 'value': 'JNJ'},
        {'label': '(BAC) Bank of America Corporation', 'value': 'BAC'},
        {'label': '(RLLCF) Rolls-Royce Holdings plc', 'value': 'RLLCF'},
        {'label': '(WMT) Walmart Inc.', 'value': 'WMT'},
        {'label': '(MA) Mastercard Incorporated', 'value': 'MA'},
        {'label': '(V) Visa Inc.', 'value': 'V'},
        {'label': '(DIS) The Walt Disney Company', 'value': 'DIS'},
        {'label': '(PG) The Procter & Gamble Company', 'value': 'PG'},
    ]

###################################################
###################################################
###################################################
############ data_creater #########################
###################################################
###################################################
###################################################

stocks_list = ["AMZN", "C", "AAPL", "IBM", "CSCO",
              "NVDA", "MSFT", "TM", "CVX", "GOOG",
              "FB", "TSLA", "JPM", "JNJ", "BAC",
              "RLLCF", "WMT", "MA", "V", "DIS", "PG"]
months_value = 29
today = date.today()
end_date = today + relativedelta(days = -27)
start_date_0 = end_date + relativedelta(months =- months_value) + relativedelta(days = 1)

all_watch_list_df = yf.download(stocks_list,
                               start=start_date_0,
                               end=end_date,
                               progress=False,
                               )['Close']

all_watch_list_last_month = yf.download(stocks_list,
                                       start=end_date,
                                       end=today,
                                       progress=False,
                                       )['Close']

s_p_500 = yf.download('^GSPC',
                               start=end_date,
                               end=today,
                               progress=False,
                               )['Close']

fig_sp = go.Figure() # create figure
fig_sp.add_trace(go.Scatter(x=s_p_500.index,
                         y=s_p_500,
                         line_color = 'green') )
fig_sp.update_traces(textposition="bottom right")      
fig_sp.update_layout(plot_layout_2)
fig_sp.update_layout(
            dict(title_text="S & P 500 stock price during future month",
                 autosize=True,
                 yaxis_title='Value of portfolio',
                 )
                )

###################################################
###################################################
###################################################
############ layout ######### #####################
###################################################
###################################################
###################################################






app.layout = html.Div(
    [
    html.Div(children = [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4("PORTFOLIO MANAGEMENT DASHBOARD"),
                                    ],
                                    className="header__title",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            "Dashboard crated by Artur, Susanna & Tigranuhi"
                                        )
                                    ],
                                    className="header__info pb-20",
                                ),
                                html.Div(
                                    [
                                        html.A(
                                            "View on GitHub",
                                            href=GITHUB_LINK,
                                            target="_blank",
                                        )
                                    ],
                                    className="header__button",
                                ),
                            ],
                            className="header pb-20",
                        ),





                        html.Div(
                            #########################################
                            # stocks_price
                            #########################################
                             [html.Div(
                                [
                                    dcc.Graph(
                                        id="stock_price",
                                    )
                                ],
                                className="graph__container",
                            ),

                            #########################################
                            # rate_return
                            #########################################

                            html.Div(
                                [
                                    dcc.Graph(
                                        id="stock_rr",
                                    )
                                ],
                                className="graph__container",
                            ),],
                            style = {'display': 'flex',
                                    'flex-flaw': 'row-wrap',}
                        ),






                        
                        html.Div(
                            #########################################
                            # graph_sharp
                            #########################################
                             [html.Div(
                                [
                                    dcc.Graph(
                                        id="sharp_graph",
                                    )
                                ],
                                className="graph__container",
                            ),

                            #########################################
                            # graph_portf
                            #########################################

                            html.Div(
                                [
                                    dcc.Graph(
                                        id="portf_graph_sharp",
                                    )
                                ],
                                className="graph__container",
                            ),
                            ],
                            style = {'display': 'flex',
                                    'flex-flaw': 'row-wrap',}
                        ),



                         html.Div(
                            #########################################
                            # graph_sharp
                            #########################################
                             [
                             html.Div(
                                [
                                    dcc.Graph(
                                        id="corr_graph",
                                    )
                                ],
                                className="graph__container",
                            ),

                            #########################################
                            # s&p500
                            #########################################

                            html.Div(
                                [
                                    dcc.Graph(
                                        id="s&p500",
                                        figure = fig_sp
                                    )
                                ],
                                className="graph__container",
                                ),
                            ],
                            style = {'display': 'flex',
                                    'flex-flaw': 'row-wrap',}
                        ),
                    ],
                    className="container",
                )
            ],
            className="two-thirds column app__left__section",
        ),


        #########################################
        # tools
        #########################################


        html.Div(
            [
                
                #########################################
                # chekclist_stocks
                #########################################

                html.Div(
                    children = [
                                html.P("Choose stocks for portfolio",
                                    className="subheader"
                                    ),
                                dcc.Checklist(
                                                id = 'checklist_stock',
                                                options=options_stocks_checklist,
                                                value=['AAPL','NVDA'],
                                                # labelStyle={'display': 'inline-block'}
                                            )
                    ],
                    className="colorscale pb-20",
                ),

                #########################################
                # date_interval
                #########################################



                html.Div(
                    children = [
                                html.P("Choose count of mounths for Sharp analysis",
                                    className="subheader"
                                    ),
                                dcc.Slider(
                                            id = 'slider_month',
                                            min=1,
                                            max=36,
                                            step=1,
                                            value=12,
                                            marks={
                                                    12: {'label': '12', 'style': {'color': '#77b0b1'}},
                                                    24: {'label': '24', 'style': {'color': '#77b0b1'}},
                                                    36: {'label': '36', 'style': {'color': '#77b0b1'}},
                                                    },
                                            # included=True,
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            )
                    ],
                    className="colorscale pb-20",
                ) ,

                #########################################
                # sharpe_statistics
                #########################################

                html.Div(
                        children=[
                                    html.P("Stock weights from Sharp",
                                            className="subheader"
                                    ),
                                    html.Div(id = 'sharp_stats')
                                ],
                                className="colorscale pb-20",
                ),


            ],
            # style = {'position': 'fixed'},

            className="one-third column app__right__section",
        ),
        ],
        style = {'display': 'flex','flex-flaw': 'row-wrap',}
        )
        # dcc.Store(id="annotation_storage"),
    ]
)







###################################################
###################################################
###################################################
############ graph_sharp ##########################
###################################################
###################################################
###################################################




@app.callback(
    [Output('sharp_graph', 'figure'),
     Output('sharp_stats','children'),
     Output('portf_graph_sharp', 'figure')],
    [Input('checklist_stock', 'value'),
     Input('slider_month', 'value')]
)
def sharp_graph(stock_list, month_value):

    start_date_2 = end_date + relativedelta(months =- month_value) + relativedelta(days = 1)
    days_interval = (end_date - start_date_2).days
    
    
    watch_df_list = yf.download(stock_list,
                           start=end_date,
                           end=end_date,
                           progress=False,
                           )['Close'][stock_list]

    watch_df_list_change = all_watch_list_df.iloc[-days_interval:,:][stock_list].pct_change()
    
    columns_list = ['portfolio_return',
                    'portfolio_st_dev']
    for i in stock_list:
        columns_list.append('weight of '+ i)
    all_portfolios=pd.DataFrame(columns=columns_list)

    number_assets = len(stock_list)

    number_porfolios = 10000

    for porfolios in range(number_porfolios):
        weight = np.random.random(number_assets)
        weight = weight / weight.sum()
        
        porfolio_return=(watch_df_list_change[1:]*weight).sum(1).mean()
        
        portfolio_var=np.dot(np.dot(weight.T,watch_df_list_change.cov()),
                                    weight)
        portfolio_st_dev = np.sqrt(portfolio_var)

        row_dict = {'portfolio_return':porfolio_return,
                    'portfolio_st_dev':portfolio_st_dev,}
        for i in range(len(stock_list)):
            row_dict['weight of '+ stock_list[i]] = weight[i]
        
        all_portfolios =all_portfolios.append(row_dict,
                                            ignore_index=True) #append row for every car

    all_portfolios['Sharpe_ratio']=all_portfolios['portfolio_return']/all_portfolios['portfolio_st_dev']
    best_sharpe=all_portfolios.iloc[all_portfolios['Sharpe_ratio'].argmax(),:]
    best_return = all_portfolios.iloc[all_portfolios['portfolio_return'].argmax(),:]
    best_sd = all_portfolios.iloc[all_portfolios['portfolio_st_dev'].argmin(),:]

    weight_list=watch_df_list_change.iloc[-1,]

    for i in range(len(best_sharpe[2:-1])):
        weight_list[i]=best_sharpe[2:-1][i]

    stats_list = []
    for i ,j in zip(weight_list.index, weight_list.values):
        stats_list.append(html.P(f"{i} >>>>> {np.round(100 * j,3)} %")) 


    fig = go.Figure() # create figure
    fig.add_trace(go.Scatter(x=all_portfolios.portfolio_st_dev,
                             y=all_portfolios.portfolio_return,mode='markers',showlegend=False) )

    fig.add_trace(go.Scatter(x=np.array(best_sharpe[1]),
                             y=np.array(best_sharpe[0]),name='Best from Sharpe',
                             marker=dict(size=[15])) )

    fig.add_trace(go.Scatter(x=np.array(best_return[1]),
                             y=np.array(best_return[0]),name='Best from Return',
                            marker=dict(size=[15])) )

    fig.add_trace(go.Scatter(x=np.array(best_sd[1]),
                             y=np.array(best_sd[0]),name='Best from SD',
                            marker=dict(size=[15]) ))

    for i in watch_df_list_change.columns:
        fig.add_trace(go.Scatter(x=np.array(np.std(watch_df_list_change[i])),
                                 y=np.array(np.mean(watch_df_list_change[i])),
                                 text=i,
                                 name=i,
                                 marker=dict(size=[20]) ))
    fig.update_traces(textposition="bottom right")      
    fig.update_layout(plot_layout_2)
    fig.update_layout(
                dict(title_text="All possible porfolios with our stocks",
                     autosize=True,
                     yaxis_title='Rate of returns',
                     xaxis_title='Standard deviation',
                     )
                    )



    count_stock={}
    for i in stock_list:
        count_stock[i] = 100000 * weight_list[i] / watch_df_list[i][-1]

    data_last_month = all_watch_list_last_month.reindex(columns=stock_list)
    data_last_month['Portfolio']=(data_last_month*count_stock.values()).sum(1)
    
    
    fig_3 = go.Figure() # create figure
    fig_3.add_trace(go.Scatter(x=data_last_month['Portfolio'].index,
                             y=data_last_month['Portfolio'],
                             line_color = 'green') )
    fig_3.update_traces(textposition="bottom right")      
    fig_3.update_layout(plot_layout_2)
    fig_3.update_layout(
                dict(title_text="Portfolio from Sharpe best weight during future months",
                     autosize=True,
                     yaxis_title='Value of portfolio',
                     # xaxis_title='Standard deviation',
                     )
                    )



    return [fig, stats_list,fig_3]


########################################################
########################################################
############## portf_graph_sharp #######################
########################################################
########################################################


def create_all_line_chart(watch_list,
                          data,
                          start_time,
                          end_time):

    fig = go.Figure() # create figure
    for i in watch_list:
        fig.add_trace(go.Scatter(x=data.index, y=data[i], name = i) )

    fig.update_layout(
        dict(title_text="STOCK DATA (from {} - {})".format(start_time,end_time),
             autosize=True,
             yaxis_title='Close price')
                        )
    fig.show()




########################################################
########################################################
############## stock_price_graph #######################
########################################################
########################################################


@app.callback(
    [Output('stock_price', 'figure'),
     Output('stock_rr','figure')],
    [Input('checklist_stock', 'value')]
)
def stock_graph(stock_list):
    fig = go.Figure() # create figure
    for i in stock_list:
        fig.add_trace(go.Scatter(x=all_watch_list_last_month.index,
                                    y=all_watch_list_last_month[i], name = i) )

    fig.update_traces(textposition="bottom right")      
    fig.update_layout(plot_layout_2)
    fig.update_layout(
                dict(title_text="Stock prices during future month",
                     autosize=True,
                     yaxis_title='Close Price',
                     # xaxis_title='Standard deviation',
                     )
                    )

    fig_2 = go.Figure() # create figure
    for i in stock_list:
        fig_2.add_trace(go.Scatter(x=all_watch_list_last_month.pct_change().index[1:],
                                    y=all_watch_list_last_month.pct_change()[i][1:], name = i) )

    fig_2.update_traces(textposition="bottom right")      
    fig_2.update_layout(plot_layout_2)
    fig_2.update_layout(
                dict(title_text="Stock rate of return during future month",
                     autosize=True,
                     yaxis_title='Rate of return',
                     # xaxis_title='Standard deviation',
                     )
                    )
    return [fig,fig_2]



@app.callback(
    Output('corr_graph','figure'),
    [Input('checklist_stock','value'),
     Input('slider_month', 'value')]
    )
def corr_graph(stock_list,month_value):

    start_date_2 = end_date + relativedelta(months =- month_value) + relativedelta(days = 1)
    days_interval = (end_date - start_date_2).days
    
    r = all_watch_list_df.iloc[-days_interval:,:][stock_list].pct_change()[1:]
    mask = np.triu(np.ones_like(r.corr(), dtype=bool))

    rLT = r.corr().mask(mask)

    heat = go.Heatmap(
        z = np.round(rLT,3),
        x = rLT.columns.values,
        y = rLT.columns.values,
        zmin = - 1, # Sets the lower bound of the color domain
        zmax = 1,
        xgap = 1, # Sets the horizontal gap (in pixels) between bricks
        ygap = 1,
        colorscale  = 'portland'
    )

    title = 'Asset Correlation Matrix'

    layout = go.Layout(
        title_text=title, 
        title_x=0.5, 
        # width=600, 
        # height=600,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        yaxis_autorange='reversed'
    )

    fig=go.Figure(data=[heat], layout=layout)
    fig.update_layout(plot_layout_2)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, port = 8085)
