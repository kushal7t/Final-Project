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

Real_Estate = pd.read_csv( 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=KIM&outputsize=full&apikey=' + api + '&datatype=csv')
Real_Estate['timestamp'] = pd.to_datetime(Real_Estate['timestamp'])
ree = Real_Estate.loc[(Real_Estate['timestamp'] >= '2020-01-22') & (Real_Estate['timestamp'] <= '2021-03-06')]
rea = ree.sort_values(by='timestamp',ascending = True)

r_ts = rea['timestamp'].to_list()
r_high = rea['high'].to_list()
r_low = rea['low'].to_list()
KIM_data = pd.DataFrame(list(zip(r_ts,r_high,r_low)), columns = ['Timestamp','KIM_High', 'KIM_Low'])

final_4 = covid_cd.merge(KIM_data,how='outer',left_on=['Timestamp'],right_on=["Timestamp"])
final_4['Real Estate'] = 'KIM'

f_ts = final_data['Timestamp'] 
f_tcs = (final_data['Total_Confirmed_Cases'] - final_data['Total_Confirmed_Cases'].mean()) / final_data['Total_Confirmed_Cases'].std()
f_tds = (final_data['Total_Deaths'] - final_data['Total_Deaths'].mean()) / final_data['Total_Deaths'].std()
fr_high = (final_data['KIM_High'] - final_data['KIM_High'].mean()) / final_data['KIM_High'].std()
fr_low = (final_data['KIM_Low'] - final_data['KIM_Low'].mean()) / final_data['KIM_Low'].std()

plt.plot(f_ts, f_tcs, label = 'Confirmed Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.title('Total Confirmed Cases vs. Total Deaths')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, fr_high, label = 'High')
plt.plot(f_ts, fr_low, label = 'Low')
plt.title('Real Estate High vs. Low')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, f_tcs, label = 'Confirmed Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.plot(f_ts, fr_high, label = 'High')
plt.plot(f_ts, fr_low, label = 'Low')
plt.title('Overall Real Estate Data with COVID')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()


                      



