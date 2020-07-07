import pandas as pd
from app import app, dashboard_backend
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


appdash = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/',
    external_stylesheets=[dbc.themes.FLATLY]
)

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


# Body
body_cities_stats = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5('Selecione uma cidade', style={'textAlign': 'left'}),
                        dcc.Dropdown(
                            id='cities-dropdown',
                            # options=[
                            #     {'label': 'Bahia', 'value': 'Bahia'},
                            #     {'label': 'Salvador', 'value': 'Salvador'},
                            #     {'label': 'Irecê', 'value': 'Irecê'},
                            # ],
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
                    style={'height': '14vh', 'textAlign': 'center'},
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
                                # '1.100.245',
                                style={'color': 'orange', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),
                        ),
                        dbc.CardFooter(['Confirmados ', dbc.Badge(id='badge-confirmed', color='warning')]),
                    ],
                    color='primary',
                    inverse=True,
                    style={'height': '14vh', 'textAlign': 'center'},
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
                                # '1.245',
                                style={'color': 'red', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),
                        ),
                        dbc.CardFooter(['Mortos ', dbc.Badge(id='badge-deaths', color='danger')]),
                    ],
                    color='primary',
                    inverse=True,
                    style={'height': '14vh', 'textAlign': 'center'},
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
                                # '4.45%',
                                style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '250%'}
                            ),

                        ),
                        # dbc.CardFooter(['Taxa de morte ', dbc.Badge('- 0.10%', color='light')]),
                        dbc.CardFooter(['Taxa de morte ']),
                    ],
                    color='primary',
                    inverse=True,
                    style={'height': '14vh', 'textAlign': 'center'},
                ),
                lg=3, xs=12,
                # style={'marginBottom': '10px'}
            ),
        ])
    ],
    fluid=True,
    style={'marginTop': '20px'}
)

body_confirm_death_table = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardBody('bla'),
                        dbc.CardFooter(
                            'Última Atualização 2020-07-02',
                            style={'textAlign': 'right', 'fontSize': 'small'})
                    ],
                    color='primary',
                    inverse=True,
                    style={'height': '60vh'},
                ),
                lg=4, xs=12,
                style={'marginBottom': '10px'}
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader('bla'),
                        dbc.CardBody('bla'),
                    ],
                    color='primary',
                    inverse=True,
                    style={'height': '60vh'}
                ),
                lg=8, xs=12,
                style={'marginBottom': '10px'}
            )
        ])
    ],
    fluid=True,
    style={'marginTop': '10px'}
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


appdash.title = 'Painel Bahia covid-19 | Dashboard'
appdash.layout = html.Div([
    html.Div(id='input', style={'display': 'none'}), navbar, body_cities_stats, body_confirm_death_table
])