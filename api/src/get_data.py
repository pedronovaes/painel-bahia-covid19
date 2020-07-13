import os
import time
import requests
import numpy as np
import pandas as pd
from datetime import datetime

PATH = 'api/data/'


# Get data from covid.io API
def get_data():
    print('[LOG] Getting data at {}'.format(datetime.now()))

    # Data backup
    os.system('cp {}dados_covid.csv {}dados_covid.csv.bkp'.format(PATH, PATH))

    df = pd.DataFrame()
    page = 1

    while True:
        print('[LOG] Requesting page {}'.format(page))
        url = 'https://brasil.io/api/dataset/covid19/caso_full/data/?page={}&state=BA'.format(page)
        response = requests.get(url=url)
        print('[LOG] {}'.format(response))

        if response.status_code != 200:
            continue

        data_ = response.json()['results']
        next_ = response.json()['next']

        df = pd.concat([df, pd.DataFrame(data_)])

        page += 1

        if next_ is None:
            break

        # Sleep time to make a new request
        # time.sleep(10)

    print('[LOG] Finishing get_data at {}'.format(datetime.now()))

    return df


# Dataprep
def dataprep():
    print('[LOG] Starting Dataprep at {}'.format(datetime.now()))

    df = pd.read_csv(PATH + 'dados_covid.csv')

    # Drop some unable columns
    cols = ['epidemiological_week', 'estimated_population_2019', 'is_repeated', 'order_for_place', 'state']
    df = df.drop(cols, axis=1)

    # Drop Importados cases
    df = df.drop(df[df['city'] == 'Importados/Indefinidos'].index)

    # Adding latitude and longitude columns
    lat_lon = pd.read_csv(PATH + 'lat_lon.csv')
    lat_lon.columns = ['city_ibge_code', 'city', 'latitude', 'longitude', 'capital', 'state']
    lat_lon = lat_lon[lat_lon['state'] == 29]
    df = df.merge(right=lat_lon[['city_ibge_code', 'latitude', 'longitude']],
                  how='left',
                  on='city_ibge_code')

    # Fill NaN city
    df['city'] = np.where(df['place_type'] == 'state', 'Bahia', df['city'])

    # Generate datasets to dashboard
    df.to_csv(PATH + 'dashboard.csv', index=False)

    cities = df[['city', 'latitude', 'longitude']].drop_duplicates() \
                                                  .sort_values(by='city') \
                                                  .reset_index(drop=True)
    cities.to_csv(PATH + 'cidades.csv', index=False)

    last_cases = df[df['is_last'] == True].sort_values(by='city').reset_index(drop=True)
    last_cases = last_cases[[
        'city', 'city_ibge_code', 'date', 'is_last', 'last_available_confirmed',
        'last_available_death_rate', 'last_available_deaths', 'new_confirmed',
        'new_deaths', 'latitude', 'longitude'
    ]]

    last_cases.to_csv(PATH + 'ultimos_casos.csv', index=False)

    print('[LOG] Finishing Dataprep at {}'.format(datetime.now()))


if __name__ == '__main__':
    # Execute every 6 hours
    while True:
        # Get data
        df = get_data()

        # Saving data
        df.to_csv(PATH + 'dados_covid.csv', index=False)

        # Preprocessing
        dataprep()

        time.sleep(1800)
