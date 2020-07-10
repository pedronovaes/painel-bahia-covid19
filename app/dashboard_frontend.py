import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app, dashboard_backend

appdash = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/',
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)

style = {
    'width': '100%',
    'height': '100%',
}

# Header
info_bar = html.Div(
    children=html.Ul(
        className='navbar-nav',
        children=[
            dbc.Button(
                children=html.A(
                    className='nav-link',
                    children='Informações',
                    href='/info'
                ),
                color='link'
            ),
            dbc.Button(
                children=html.A(
                    className='nav-link',
                    children='Receber Notificações',
                    href='/updates'
                ),
                color='link',
            ),
        ]
    )
)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand(
                        children=[
                            'Painel Bahia ',
                            html.Span(
                                className='badge badge-pill badge-danger',
                                children='covid-19',
                            ),
                        ],
                        className="")
                    ),
                ],
                align='center',
                no_gutters=True,
            ),
            href='/index',
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(info_bar, id="navbar-collapse", navbar=True),
    ]),
    color="primary",
    dark=True,
)


# Callback to collapse navbar
@appdash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


body_stats = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5('Selecione uma cidade', style={'textAlign': 'left'}),
                        dcc.Dropdown(
                            id='cities-dropdown',
                            value='Bahia',
                            clearable=False,
                            searchable=True,
                            style={
                                'color': '#1F242D',
                                'marginTop': '15px'
                            },
                        )
                    ]),
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%', 'textAlign': 'center'},
                ),
                lg=3, xs=12,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            html.H3(
                                id='ind-confirmed',
                                style={'color': 'orange', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),
                        ),
                        dbc.CardFooter(['Confirmados ', dbc.Badge(id='badge-confirmed', color='warning')]),
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%', 'textAlign': 'center'},
                ),
                lg=3, xs=12,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            html.H3(
                                id='ind-deaths',
                                style={'color': 'red', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),
                        ),
                        dbc.CardFooter(['Mortos ', dbc.Badge(id='badge-deaths', color='danger')]),
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%', 'textAlign': 'center'},
                ),
                lg=3, xs=12,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            html.H3(
                                id='ind-rate',
                                style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),

                        ),
                        # dbc.CardFooter(['Taxa de morte ', dbc.Badge('- 0.10%', color='light')]),
                        dbc.CardFooter(['Taxa de mortalidade ']),
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%', 'textAlign': 'center'},
                ),
                lg=3, xs=12,
                style={'marginBottom': '10px'}
            ),
        ])
    ],
    fluid=True,
    style={'marginTop': '20px'},
)


# Callback to show all cities that contains covid-19 cases
@appdash.callback(
    Output(component_id='cities-dropdown', component_property='options'),
    [Input(component_id='input', component_property='children')]
)
def update_cities_options(a):
    df = pd.read_csv('data/cities.csv')
    options = [{'label': i, 'value': i} for i in df['city'].unique()]
    return options


# Callback to update city stats
@appdash.callback(
    [
        Output(component_id='ind-confirmed', component_property='children'),
        Output(component_id='ind-deaths', component_property='children'),
        Output(component_id='ind-rate', component_property='children'),
        Output(component_id='badge-confirmed', component_property='children'),
        Output(component_id='badge-deaths', component_property='children'),
    ],
    [Input(component_id='cities-dropdown', component_property='value')]
)
def update_outputs(city):
    df = pd.read_csv('data/new.csv')
    return dashboard_backend.news_stats(df, city)


body_table_mapbox = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            id='cities-table'
                        ),
                        dbc.CardFooter(
                            id='last-update',
                            style={'textAlign': 'right', 'fontSize': 'small'})
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%'},
                ),
                lg=4, xs=12,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader('Casos', style={'fontWeight': 'bold'}),
                        dbc.CardBody(id='cities-mapbox', style={'padding': '0rem'}),
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%'},
                ),
                lg=8, xs=12,
                style={'marginBottom': '10px'}
            ),
        ])
    ],
    fluid=True,
    style={'marginTop': '10px'}
)


@appdash.callback(
    [
        Output(component_id='cities-table', component_property='children'),
        Output(component_id='last-update', component_property='children'),
        Output(component_id='cities-mapbox', component_property='children'),
    ],
    [Input(component_id='input', component_property='children')]
)
def update_table_mapbox(a):
    df_cities = pd.read_csv('data/indicators.csv')
    df_mapbox = pd.read_csv('data/mapbox.csv')

    table, last_update = dashboard_backend.news_table(df_cities)
    mapbox = dashboard_backend.news_mapbox(df_mapbox)

    return table, last_update, mapbox
    # return mapbox


body_graphs = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody('bla')
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%'}
                ),
                lg=4,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody('bla')
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%'}
                ),
                lg=4,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody('bla')
                    ],
                    color='primary',
                    inverse=True,
                    style={'width': '100%', 'height': '100%'}
                ),
                lg=4,
                style={'marginBottom': '10px'}
            ),
        ])
    ],
    fluid=True,
    style={'marginTop': '10px'}
)

appdash.title = 'Painel Bahia covid-19 | Dashboard'
appdash.layout = html.Div([
    html.Div(id='input', style={'display': 'none'}),
    navbar,
    body_stats,
    body_table_mapbox,
    body_graphs
])
