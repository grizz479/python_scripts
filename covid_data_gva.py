#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import os
import datetime
import os
import urllib, urllib.request, json

url_2021 = "https://dadesobertes.gva.es/api/3/action/package_show?id=covid-19-casos-confirmats-pcr-casos-pcr-ultims-14-dies-i-persones-mortes-per-departament-2021"
url_2020 = "https://dadesobertes.gva.es/api/3/action/package_show?id=covid-19-casos-confirmats-pcr-casos-pcr-ultims-14-dies-i-persones-mortes-per-departament-2020"
response_2021 = urllib.request.urlopen(url_2021)
response_2020 = urllib.request.urlopen(url_2020)
covid_dat_2021 = json.loads(response_2021.read())
covid_dat_2020 = json.loads(response_2020.read())
covid_dat_2021 = pd.DataFrame(covid_dat_2021['result']['resources'])
covid_dat_2020 = pd.DataFrame(covid_dat_2020['result']['resources'])
covid_dat_2020['Fecha'] = covid_dat_2020['description'].str.extract(pat="([0-9][0-9][0-9].{7})")
covid_dat_2020['Fecha'] = pd.to_datetime(covid_dat_2020['Fecha'], )
covid_dat_2021['Fecha'] = covid_dat_2021['description'].str.extract(pat="([0-9][0-9][0-9].{7})")
covid_dat_2021['Fecha'] = pd.to_datetime(covid_dat_2021['Fecha'])
nombres_fecha = covid_dat_2020['Fecha']
df_2020 = pd.DataFrame()
for i, n in covid_dat_2020.iterrows():
    tmp = pd.read_csv(covid_dat_2020['url'][i], sep=";")
    tmp['Fecha'] = nombres_fecha[i]
    df_2020 = df_2020.append(tmp)
print('done 2020')
nombres_fecha = covid_dat_2021['Fecha']
df_2021 = pd.DataFrame()
for i, n in covid_dat_2021.iterrows():
    tmp = pd.read_csv(covid_dat_2021['url'][i], sep=";")
    tmp['Fecha'] = nombres_fecha[i]
    df_2021 = df_2021.append(tmp)
print('done 2021')
df = df_2020.append(df_2021)
# Corregir huecos y notación. Coerce tipos numéricos
df['Incidència acumulada PCR+'].replace({' ': ''}, regex=True, inplace=True)
df['Incidència acumulada PCR+'].replace({',': '.'}, regex=True, inplace=True)
df['Incidència acumulada PCR+14'].replace({' ': ''}, regex=True, inplace=True)
df['Incidència acumulada PCR+14'].replace({',': '.'}, regex=True, inplace=True)
df['Taxa de defunció'].replace({' ': ''}, regex=True, inplace=True)
df['Taxa de defunció'].replace({',': '.'}, regex=True, inplace=True)
df['Incidència acumulada PCR+'] = df['Incidència acumulada PCR+'].apply(pd.to_numeric, errors='coerce')
df['Incidència acumulada PCR+14'] = df['Incidència acumulada PCR+14'].apply(pd.to_numeric, errors='coerce')
df['Taxa de defunció'] = df['Taxa de defunció'].apply(pd.to_numeric, errors='coerce')
df.set_index('Fecha', inplace=True)
def list_full_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]
 
filenames = list_full_paths("/home/pi/covid_data/")
filenames.sort()
last_file = filenames[-1]
file_name= "data_agg_covid_CV_"+str(df.index[-1])[:10]
file_path="/home/pi/covid_data/"+file_name+".pickle"
if file_path != last_file:
    df.to_pickle(file_path)
    print('Saved')
else:
    print('Data already up to date')