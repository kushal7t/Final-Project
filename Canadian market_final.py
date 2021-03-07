import pandas as pd
from matplotlib import pyplot as plt
from alpha_vantage.timeseries import TimeSeries

api = 'KZPT32AEEXXIV6Y2'

deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirm = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
Canadian_markert = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=' + api + '&datatype=csv')

total_c = confirm.sum(axis = 0, skipna = True)
totalc = total_c.to_list()
total_d = deaths.sum(axis = 0, skipna = True)
totald = total_d.to_list()

timestamp = deaths.columns.to_list()
del timestamp[0:4]
del totalc[0:3]
del totald[0:3]

Canadian_markert['timestamp'] = pd.to_datetime(Canadian_markert['timestamp'])
c_mark = Canadian_markert.loc[(Canadian_markert['timestamp'] >= '2020-01-22') & (Canadian_markert['timestamp'] <= '2021-03-06')]
c_market = c_mark.sort_values(by='timestamp',ascending = True)

shop_ts = c_mark['timestamp'].to_list()
shop_high = c_mark['high'].to_list()
shop_low = c_mark['low'].to_list()

covid_cd = pd.DataFrame(list(zip(timestamp,totalc,totald)), columns = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths'])
covid_cd['Total_Confirmed_Cases'] = covid_cd.Total_Confirmed_Cases.astype('int')
covid_cd['Total_Deaths'] = covid_cd.Total_Deaths.astype('int')
covid_cd['Timestamp'] = pd.to_datetime(covid_cd['Timestamp'])

SHOP_data = pd.DataFrame(list(zip(shop_ts,shop_high,shop_low)), columns = ['Timestamp', 'High', 'Low'])

final_shop = covid_cd.merge(SHOP_data,how='outer',left_on=['Timestamp'],right_on=["Timestamp"])
final_shop['Stock'] = 'SHOP'

final_cols = ["Timestamp","Total_Confirmed_Cases","Total_Deaths","Stock","High","Low"]
final_CM = final_shop.reindex(columns = final_cols)

final_CM.to_csv('Final_Canadian_Market.csv')
print(final_CM)

f_ts = final_shop['Timestamp'] 
f_tcs = (final_shop['Total_Confirmed_Cases'] - final_shop['Total_Confirmed_Cases'].mean()) / final_shop['Total_Confirmed_Cases'].std()
f_tds = (final_shop['Total_Deaths'] - final_shop['Total_Deaths'].mean()) / final_shop['Total_Deaths'].std()
f_high = (final_shop['High'] - final_shop['High'].mean()) / final_shop['High'].std()
f_low = (final_shop['Low'] - final_shop['Low'].mean()) / final_shop['Low'].std()

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