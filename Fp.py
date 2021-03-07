import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

api = 'C35O2SUDZPRYANJP'

deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirm = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

total_c = confirm.sum(axis = 0, skipna = True)
totalc = total_c.to_list()

total_d = deaths.sum(axis = 0, skipna = True)
totald = total_d.to_list()

timestamp = deaths.columns.to_list()
del timestamp[0:4]
del totalc[0:3]
del totald[0:3]

covid_cd = pd.DataFrame(list(zip(timestamp,totalc,totald)), columns = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths'])
covid_cd['Total_Confirmed_Cases'] = covid_cd.Total_Confirmed_Cases.astype('int')
covid_cd['Total_Deaths'] = covid_cd.Total_Deaths.astype('int')
covid_cd['Timestamp'] = pd.to_datetime(covid_cd['Timestamp'])
