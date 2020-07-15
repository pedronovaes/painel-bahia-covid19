import os
import time
import requests
import logging
import numpy as np
import pandas as pd
from datetime import datetime

DATABASE_PATH = 'api/data/'
SRC_PATH = 'api/src/'

global df

logging.basicConfig(
    filename=SRC_PATH + 'file.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)


# Get data from data.brasil.io API
def request_from_api():
    logging.info('(request_from_api):\t\tStarting')

    page = 1
    temp = pd.DataFrame()

    while True:
        logging.info('(request_from_api):\t\tRequesting page {}'.format(page))

        url = 'https://brasil.io/api/dataset/covid19/caso_full/data/?page={}&state=BA'.format(page)
        response = requests.get(url=url)
        logging.info('(request_from_api):\t\t{}'.format(response))

        # If not okay, try again
        if response.status_code != 200:
            continue

        data_ = response.json()['results']
        next_ = response.json()['next']
        temp = pd.concat([temp, pd.DataFrame(data_)])

        page += 1

        # If it is the last page
        if next_ is None:
            break

        # Sleep time to make a new request
        # time.sleep(10)

    logging.info('(request_from_api):\t\tFinishing')

    return temp


# Dataprep
def dataprep():
    logging.info('(dataprep):\t\tStarting')

    # Writing df
    df.to_csv(DATABASE_PATH + 'dados_covid.csv', index=False)

    # Drop some unable columns
    cols = [
        'epidemiological_week', 'estimated_population_2019',
        'is_repeated', 'order_for_place', 'state'
    ]
    temp = df.drop(cols, axis=1).copy()

    # Drop Importados cases
    # temp = temp.drop(temp[temp['city'] == 'Importados/Indefinidos'].index)
    temp = temp[temp['city'] != 'Importados/Indefinidos']

    # Adding latitude and longitude columns
    lat_lon = pd.read_csv(DATABASE_PATH + 'lat_lon.csv')
    lat_lon.columns = [
        'city_ibge_code', 'city', 'latitude', 'longitude',
        'capital', 'state'
    ]
    lat_lon = lat_lon[lat_lon['state'] == 29]
    temp = temp.merge(
        right=lat_lon[['city_ibge_code', 'latitude', 'longitude']],
        how='left',
        on='city_ibge_code'
    )

    # Fill Nan city
    temp['city'] = np.where(temp['place_type'] == 'state', 'Bahia', temp['city'])

    logging.info('(dataprep):\t\tFinishing')

    return temp


def save_data():
    logging.info('(save_data):\t\tStarting')

    df.to_csv(DATABASE_PATH + 'dashboard.csv', index=False)
    # print(temp.head())

    cities = df[['city', 'latitude', 'longitude']].drop_duplicates() \
                                                  .sort_values(by='city') \
                                                  .reset_index(drop=True) \
                                                  .copy()
    cities.to_csv(DATABASE_PATH + 'cidades.csv', index=False)

    logging.info('(save_data):\t\tShape Database Cidades: {}'.format(cities.shape))

    last_cases = df[df['is_last'] == True].sort_values(by='city') \
                                          .reset_index(drop=True)
    last_cases = last_cases[[
        'city', 'city_ibge_code', 'date', 'is_last', 'last_available_confirmed',
        'last_available_death_rate', 'last_available_deaths', 'new_confirmed',
        'new_deaths', 'latitude', 'longitude'
    ]]
    last_cases.to_csv(DATABASE_PATH + 'ultimos_casos.csv', index=False)

    logging.info('(save_data):\t\tShape Database Ultimos casos: {}'.format(last_cases.shape))

    logging.info('(save_data):\t\tFinishing')


if __name__ == '__main__':
    # Execute every 6 hours
    while True:
        logging.info('(main):\t\tStarting')

        # Get data
        df = request_from_api()

        # Save raw dataframe and Preprocessing
        df = dataprep()

        # Save dashboards dataframes
        save_data()

        current_time = datetime.now().strftime('%H:%M')
        current_time = pd.DataFrame({'current_time': [current_time]})
        current_time.to_csv(DATABASE_PATH + 'current_time.csv', index=False)

        logging.info('(main):\t\tFinishing')

        time.sleep(21600)
