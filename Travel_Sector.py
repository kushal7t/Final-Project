import pandas as pd
from matplotlib import pyplot as plt
from alpha_vantage.timeseries import TimeSeries

api = '0J3W59536FNCYVCG'

deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirm = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
Travel_sector = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LUV&outputsize=full&apikey=' + api + '&datatype=csv')

total_c = confirm.sum(axis = 0, skipna = True)
totalc = total_c.to_list()
total_d = deaths.sum(axis = 0, skipna = True)
totald = total_d.to_list()

timestamp = deaths.columns.to_list()
del timestamp[0:4]
del totalc[0:3]
del totald[0:3]

Travel_sector['timestamp'] = pd.to_datetime(Travel_sector['timestamp'])
Travel = Travel_sector.loc[(Travel_sector['timestamp'] >= '2020-01-22') & (Travel_sector['timestamp'] <= '2021-03-06')]
Travel = Travel.sort_values(by='timestamp',ascending = True)

LUV_ts = Travel['timestamp'].to_list()
LUV_high = Travel['high'].to_list()
LUV_low = Travel['low'].to_list()

covid_cd = pd.DataFrame(list(zip(timestamp,totalc,totald)), columns = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths'])
covid_cd['Total_Confirmed_Cases'] = covid_cd.Total_Confirmed_Cases.astype('int')
covid_cd['Total_Deaths'] = covid_cd.Total_Deaths.astype('int')
covid_cd['Timestamp'] = pd.to_datetime(covid_cd['Timestamp'])

Travel_data = pd.DataFrame(list(zip(LUV_ts,LUV_high,LUV_low)), columns = ['Timestamp', 'High', 'Low'])

final = covid_cd.merge(Travel_data,how='outer',left_on=['Timestamp'],right_on=["Timestamp"])
final['Travel'] = 'LUV'

final_cols = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths', 'Travel', 'High', 'Low']
final_Travel = final.reindex(columns = final_cols)

final_Travel.to_csv("Final_Data_Travel.csv")
print(final_Travel)

f_ts = final['Timestamp'] 
f_tcs = (final['Total_Confirmed_Cases'] - final['Total_Confirmed_Cases'].mean()) / final['Total_Confirmed_Cases'].std()
f_tds = (final['Total_Deaths'] - final['Total_Deaths'].mean()) / final['Total_Deaths'].std()
f_high = (final['High'] - final['High'].mean()) / final['High'].std()
f_low = (final['Low'] - final['Low'].mean()) / final['Low'].std()

plt.plot(f_ts, f_tcs, label = 'Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.title('Total cases vs. Total deaths')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, f_high, label = 'High')
plt.plot(f_ts, f_low, label = 'Low')
plt.title('High vs. Low')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, f_tcs, label = 'Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.plot(f_ts, f_high, label = 'High')
plt.plot(f_ts, f_low, label = 'Low')
plt.title('Overall')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

