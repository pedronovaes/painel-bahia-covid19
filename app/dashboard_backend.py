import dash_table
import dash_core_components as dcc
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
        lat='latitude',
        lon='longitude',
        color='last_available_confirmed',
        size=df['last_available_confirmed'] ** 0.37,
        hover_name='city',
        hover_data={
            'last_available_confirmed': True,
            'last_available_deaths': True
        },
        zoom=6,
        # height=600,
        size_max=50,
    )

    fig.update_layout(
        mapbox_style='streets',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        coloraxis_showscale=False,
    )

    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br><br>Confirmados: %{marker.color}<br>Mortes: %{customdata[1]}<extra></extra>'
    )

    fig = dcc.Graph(figure=fig, config={'displayModeBar': False})

    return fig


def news_table(df):
    last_update = df['date'].unique()[-1]

    df = df[['city', 'last_available_confirmed', 'last_available_deaths']]
    df = df.sort_values(by='last_available_confirmed', ascending=False)
    df = df.drop(df[df['city'].str.contains('Bahia|Importados', regex=True)].index)

    table = dash_table.DataTable(
        columns=[
            {'name': 'Cidade', 'id': 'city'},
            {'name': 'Confirmados', 'id': 'last_available_confirmed'},
            {'name': 'Mortos', 'id': 'last_available_deaths'},
        ],
        data=df.head(10).to_dict('records'),
        editable=False,
        style_as_list_view=True,
        style_header={
            'backgroundColor': '#2C3E50',
            'border': '#2C3E50',
            'fontWeight': 'bold',
            'font': 'Lato, sans-serif',
            # "height": "2vw",
        },
        style_cell={
            'font-family': 'Lato, sans-serif',
            # 'font-size': '1.1vw',
            'border-bottom': '0.01rem solid #2C3E50',
            'backgroundColor': '#2C3E50',
            'height': '1.9vw',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'city'},
                'textAlign': 'left',
            },
            {
                'if': {'column_id': 'last_available_confirmed'},
                'color': 'orange',
                'textAlign': 'center',
            },
            {
                'if': {'column_id': 'last_available_deaths'},
                'color': '#E74C3C',
                'textAlign': 'center',
            },
        ],
    )

    last_update = last_update.split('-')
    last_update = str(last_update[2] + '-' + last_update[1] + '-' + last_update[0])

    last_update = 'Última Atualização: ' + last_update

    return table, last_update


def news_graph(df, city):
    temp = df[df['city'] == city]

    # Confirmed cases
    confirmed_cases = px.line(temp, x='date', y='last_available_confirmed')
    confirmed_cases.update_layout(
        yaxis_title='Número de casos',
        xaxis_title='',
        margin={'r': 20, 't': 0, 'l': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={'linecolor': 'rgba(0,0,0,0)'},
        hoverlabel={'font': {'color': 'white'}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={'tickformat': '%d/%m'},
        font=dict(family='Roboto, sans-serif', size=12, color='#f4f4f4'),
        autosize=True,
        showlegend=False,
        legend_orientation='h',
    )
    confirmed_cases.update_traces(
        hovertemplate='Data: %{x}<br>Confirmados: %{y}<extra></extra>'
    )

    confirmed_cases = dcc.Graph(figure=confirmed_cases, config={'displayModeBar': False})

    # Daily cases
    daily_cases = px.line(temp, x='date', y='new_confirmed')
    daily_cases.update_layout(
        yaxis_title='Número de casos diários',
        xaxis_title='',
        margin={'r': 20, 't': 0, 'l': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={'linecolor': 'rgba(0,0,0,0)'},
        hoverlabel={'font': {'color': 'white'}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={'tickformat': '%d/%m'},
        font=dict(family='Roboto, sans-serif', size=12, color='#f4f4f4'),
        autosize=True,
        showlegend=False,
        legend_orientation='h',
    )
    daily_cases.update_traces(
        hovertemplate='Data: %{x}<br>Confirmados: %{y}<extra></extra>'
    )
    daily_cases = dcc.Graph(figure=daily_cases, config={'displayModeBar': False})

    # Deaths cases
    deaths_cases = px.line(temp, x='date', y='last_available_deaths')
    deaths_cases.update_layout(
        yaxis_title='Número de mortes',
        xaxis_title='',
        margin={'r': 20, 't': 0, 'l': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={'linecolor': 'rgba(0,0,0,0)'},
        hoverlabel={'font': {'color': 'white'}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={'tickformat': '%d/%m'},
        font=dict(family='Roboto, sans-serif', size=12, color='#f4f4f4'),
        autosize=True,
        showlegend=False,
        legend_orientation='h'
    )
    deaths_cases.update_traces(
        hovertemplate='Data: %{x}<br>Mortes: %{y}<extra></extra>'
    )
    deaths_cases = dcc.Graph(figure=deaths_cases, config={'displayModeBar': False})

    return confirmed_cases, daily_cases, deaths_cases
