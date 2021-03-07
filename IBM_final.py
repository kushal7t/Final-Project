import pandas as pd
from matplotlib import pyplot as plt
from alpha_vantage.timeseries import TimeSeries

api = 'C8TNJKUP66PXAD3G'

deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirm = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
american_markert = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=' + api + '&datatype=csv')

total_c = confirm.sum(axis = 0, skipna = True)
totalc = total_c.to_list()
total_d = deaths.sum(axis = 0, skipna = True)
totald = total_d.to_list()

timestamp = deaths.columns.to_list()
del timestamp[0:4]
del totalc[0:3]
del totald[0:3]

american_markert['timestamp'] = pd.to_datetime(american_markert['timestamp'])
a_mark = american_markert.loc[(american_markert['timestamp'] >= '2020-01-22') & (american_markert['timestamp'] <= '2021-03-06')]
a_market = a_mark.sort_values(by='timestamp',ascending = True)

ibm_ts = a_mark['timestamp'].to_list()
ibm_high = a_mark['high'].to_list()
ibm_low = a_mark['low'].to_list()

covid_cd = pd.DataFrame(list(zip(timestamp,totalc,totald)), columns = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths'])
covid_cd['Total_Confirmed_Cases'] = covid_cd.Total_Confirmed_Cases.astype('int')
covid_cd['Total_Deaths'] = covid_cd.Total_Deaths.astype('int')
covid_cd['Timestamp'] = pd.to_datetime(covid_cd['Timestamp'])

IBM_data = pd.DataFrame(list(zip(ibm_ts,ibm_high,ibm_low)), columns = ['Timestamp', 'High', 'Low'])

final_ibm = covid_cd.merge(IBM_data,how='outer',left_on=['Timestamp'],right_on=["Timestamp"])
final_ibm['Stock'] = 'IBM'

final_cols = ["Timestamp","Total_Confirmed_Cases","Total_Deaths","Stock","High","Low"]
final_AME = final_ibm.reindex(columns = final_cols)

final_AME.to_csv('Final_Americal_Market.csv')
print(final_AME)

f_ts = final_ibm['Timestamp'] 
f_tcs = (final_ibm['Total_Confirmed_Cases'] - final_ibm['Total_Confirmed_Cases'].mean()) / final_ibm['Total_Confirmed_Cases'].std()
f_tds = (final_ibm['Total_Deaths'] - final_ibm['Total_Deaths'].mean()) / final_ibm['Total_Deaths'].std()
f_high = (final_ibm['High'] - final_ibm['High'].mean()) / final_ibm['High'].std()
f_low = (final_ibm['Low'] - final_ibm['Low'].mean()) / final_ibm['Low'].std()

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