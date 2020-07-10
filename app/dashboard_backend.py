import numpy as np
import pandas as pd
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px


def news_stats(df, city):
    city_stats = df[df['city'] == city].values[0]

    ind_confirmed = city_stats[4]
    ind_deaths = city_stats[6]
    ind_rate = str(round(ind_deaths * 100 / ind_confirmed, 2)) + '%'

    new_confirmed = city_stats[7]

    if new_confirmed > 0:
        new_confirmed = '+' + str(new_confirmed) + ' novos'
    else:
        new_confirmed = str(new_confirmed) + ' novos'

    new_deaths = city_stats[8]
    if new_deaths > 0:
        new_deaths = '+' + str(new_deaths) + ' novos'
    else:
        new_deaths = str(new_deaths) + ' novos'

    # print(ind_confirmed, ind_deaths, ind_rate, new_confirmed, new_deaths)

    return [ind_confirmed, ind_deaths, ind_rate, new_confirmed, new_deaths]


def news_mapbox(df):
    px.set_mapbox_access_token('pk.eyJ1IjoicGVkcm9ub3ZhZXMiLCJhIjoiY2tjNXBmNW03MDFhbjJycGIwMDU1Y3JpMiJ9.bCPPlCoJ4RmUyAXqj3b3PQ')

    fig = px.scatter_mapbox(
        data_frame=df,
        lat='lat',
        lon='lon',
        color='last_available_confirmed',
        size=df['last_available_confirmed'] ** 0.37,
        hover_name='city',
        # hover_data=['city', 'last_available_confirmed'],
        zoom=6,
        height=475,
        size_max=50,
    )

    fig.update_layout(
        mapbox_style='streets',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        coloraxis_showscale=False,
    )

    fig = dcc.Graph(figure=fig)

    return [fig]
