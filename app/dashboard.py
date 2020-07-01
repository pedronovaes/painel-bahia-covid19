from app import app
from dash import Dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

appdash = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

info_bar = html.Div(
    children=html.Ul(
        className='navbar-nav',
        children=[
            html.Button(
                type='button',
                className='btn btn-link',
                children=html.Li(
                    className='nav-item',
                    children=html.A(
                        className='nav-link',
                        children='Informações',
                        href='/info'
                    )
                )
            ),
            html.Button(
                type='button',
                className='btn btn-link',
                children=html.Li(
                    className='nav-item',
                    children=html.A(
                        className='nav-link',
                        children='Receber Notificações',
                        href='/updates'
                    )
                )
            )
        ]
    )
)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row(
                [
                    # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
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
    color="dark",
    dark=True,
)


# add callback for toggling the collapse on small screens
@appdash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


appdash.layout = html.Div(navbar)
