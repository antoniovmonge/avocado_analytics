import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def Header(app):
    return html.Div(get_header(app))


def get_header(app):
    header = html.Div(
        [
            dbc.Row(
                [
                    html.Div(
                        html.Img(
                            src=app.get_asset_url("antonio_green_transparent.svg"),
                            className="logo",
                        ),
                        className='three columns'
                    ), 
                    html.Div(
                        [
                            html.H1(
                                children="Avocado 🥑 Analytics", className="header-title"
                            ),
                            html.P(
                                children="Analyze the behavior of avocado prices and the number of avocados sold in the US between 2015 and 2018",
                                className="header-description",
                            ),
                            
                        ],className='seven columns'
                    ),
                    html.Div(
                        html.A(
                                html.Button("Portfolio", id="learn-more-button"),
                                href="https://antonio-vm-portfolio.herokuapp.com/",
                            ),
                            # className='three columns'
                    )
                    
                ],
                
            ),
            # html.Div(
            #     [
            #         html.Div(
            #             [html.H5("E-Commerce Analysis")],
            #             className="seven columns main-title",
            #         )
            #     ],
            #     className="twelve columns",
            #     style={"padding-left": "0"},
            # ),
        ],
        className="row",
    )
    return header