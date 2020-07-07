import numpy as np
import pandas as pd


def news_stats(df, city):
    city_stats = df[df['city'] == city].values[0]

    ind_confirmed = city_stats[5]
    ind_deaths = city_stats[7]
    ind_rate = str(round(ind_deaths * 100 / ind_confirmed, 2)) + '%'

    new_confirmed = city_stats[8]

    if new_confirmed > 0:
        new_confirmed = '+ ' + str(new_confirmed) + ' novos'
    else:
        new_confirmed = str(new_confirmed) + ' novos'

    new_deaths = city_stats[9]
    if new_deaths > 0:
        new_deaths = '+ ' + str(new_deaths) + ' novos'
    else:
        new_deaths = str(new_deaths) + ' novos'

    # print(ind_confirmed, ind_deaths, ind_rate, new_confirmed, new_deaths)

    return [ind_confirmed, ind_deaths, ind_rate, new_confirmed, new_deaths]
