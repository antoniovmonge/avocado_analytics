import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

from utils import Header

data = pd.read_csv("raw_data/avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Avocado Analytics"

app.layout = html.Div(
    [
        html.Div([Header(app)]),
        
        
                # html.P(children="🥑", className="header-emoji"),
                # html.H1(
                #     children="Avocado 🥑 Analytics", className="header-title"
                # ),
                # html.P(
                #     children="Analyze the behavior of avocado prices and the number of avocados sold in the US between 2015 and 2018",
                #     className="header-description",
                # ),
        # DROPDOWNS
        dbc.Row(
            html.Div(
            children=[
                # DROPDOWN REGION
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # DROPDOWN TYPE
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                # DATE SELECTOR
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range (01/04/2015 - 03/25/2018)",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        )
        ),
        
        
        
        # CHARTS
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='figure1', config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # # CHART PRICES
                # html.Div(
                #     children=dcc.Graph(
                #         id="price-chart", config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
                # # CHART SOLD
                # html.Div(
                #     children=dcc.Graph(
                #         id="volume-chart", config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
            ],
            className="wrapper",
        ),
        
    ],
    className="page",
)
        



@app.callback(
    Output('figure1','figure'),
    # [Output("figure1",'figure'), Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    # price_chart_figure
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Scatter(
            x=filtered_data["Date"],
            y= filtered_data["AveragePrice"],
            name='Price',
            hovertemplate="$%{y:.2f}<extra></extra>",
            line=dict(color="#17B897"),
            mode="lines",
        ),
        secondary_y=False,
    )
    fig1.add_trace(
        go.Scatter(
            x=filtered_data["Date"],
            y=filtered_data["Total Volume"],
            name='Sales',
            mode="lines",
        ),
        secondary_y=True,
    )
    fig1.update_layout(
        autosize=True,
        width=1024,
        height=550,
        plot_bgcolor='rgba(0,0,0,0.02)',
        title_text="Average Price VS Sales",
        font=dict(
        family="Lato, Sans-Serif",
        # size=18,
        # color="RebeccaPurple"
        ),
        showlegend = True,
        hovermode  = 'x',
        legend=dict(
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
            )
        ),
        margin=dict(l=100, r=50, b=100, t=100, pad=0),
        yaxis=dict(
            showline=True,
            type='linear',
            zeroline=False
        ),
        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(
                    count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"
                    ),
                dict(
                    count=3,
                    label='3m',
                    step='month',
                    stepmode='backward'
                ),
                dict(
                    count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"
                    ),
                dict(
                    count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )
    # Set x-axis title
    fig1.update_xaxes(
        # title_text="Date",
        gridcolor='rgba(0,0,0,0.05)'
        )
    # Set y-axes titles
    fig1.update_yaxes( # y axes PRICE
        title_text="PRICE",
        secondary_y=False,
        tickprefix='$',
        titlefont=dict(
            color="#17B897"
        ),
        tickfont=dict(
            color="#17B897"
        ),
        gridcolor='rgba(0,0,0,0.05)'
        )
    fig1.update_yaxes( # y axes SALES
        title_text="SALES",
        secondary_y=True,
        titlefont=dict(
            color="#E12D39"
        ),
        tickfont=dict(
            color="#E12D39"
        ),
        gridcolor='rgba(0,0,0,0.05)'
    )

    
    # price_chart_figure = {
    #         "data": [
    #             {
    #                 "x": filtered_data["Date"],
    #                 "y": filtered_data["AveragePrice"],
    #                 "type": "lines",
    #                 "hovertemplate": "$%{y:.2f}<extra></extra>",
    #             },
    #         ],
    #         "layout": {
    #             "title": {
    #                 "text": "Average Price of Avocados",
    #                 "x": 0.05,
    #                 "xanchor": "left",
    #             },
    #             "xaxis": {"fixedrange": True},
    #             "yaxis": {"tickprefix": "$", "fixedrange": True},
    #             "colorway": ["#17B897"],
    #         },
    #     }

    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Date"],
    #             "y": filtered_data["Total Volume"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }
    # return fig1, price_chart_figure, volume_chart_figure
    return fig1


if __name__ == "__main__":
    app.run_server(debug=True)