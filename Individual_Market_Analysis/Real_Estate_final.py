import pandas as pd
import matplotlib.pyplot as plt
import alpha_vantage


api = 'H957G6TC1ODM4ZCU' 
Real_Estate = pd.read_csv( 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=KIM&outputsize=full&apikey=' + api + '&datatype=csv')
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

Real_Estate['timestamp'] = pd.to_datetime(Real_Estate['timestamp'])
ree = Real_Estate.loc[(Real_Estate['timestamp'] >= '2020-01-22') & (Real_Estate['timestamp'] <= '2021-03-06')]
rea = ree.sort_values(by='timestamp',ascending = True)

covid_cd = pd.DataFrame(list(zip(timestamp,totalc,totald)), columns = ['Timestamp', 'Total_Confirmed_Cases', 'Total_Deaths'])

covid_cd['Total_Confirmed_Cases'] = covid_cd.Total_Confirmed_Cases.astype('int')
covid_cd['Total_Deaths'] = covid_cd.Total_Deaths.astype('int')
covid_cd['Timestamp'] = pd.to_datetime(covid_cd['Timestamp'])
print(covid_cd)

r_ts = rea['timestamp'].to_list()
r_high = rea['high'].to_list()
r_low = rea['low'].to_list()
met_data = pd.DataFrame(list(zip(r_ts,r_high,r_low)), columns = ['Timestamp','High', 'Low'])
print(met_data)

final= covid_cd.merge(met_data,how='outer',left_on=['Timestamp'],right_on=["Timestamp"])
final['Real Estate'] = 'KIM'

final.to_csv('Real_Estate_final.csv')
print(final)

df = pd.read_csv('Real_Estate_final.csv')
columns_titles = ["Timestamp","Total_Confirmed_Cases","Total_Deaths","Real Estate","High","Low"]
df_reorder=final.reindex(columns=columns_titles)
df_reorder.to_csv('Real_Estate_final.csv', index=False)
print(df_reorder)

f_ts = final['Timestamp'] 
f_tcs = (final['Total_Confirmed_Cases'] - final['Total_Confirmed_Cases'].mean()) / final['Total_Confirmed_Cases'].std()
f_tds = (final['Total_Deaths'] - final['Total_Deaths'].mean()) / final['Total_Deaths'].std()
f_high = (final['High'] - final['High'].mean()) / final['High'].std()
f_low = (final['Low'] - final['Low'].mean()) / final['Low'].std()

plt.plot(f_ts, f_tcs, label = 'Confirmed Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.title('Total Confirmed Cases vs. Total Deaths')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, f_high, label = 'High')
plt.plot(f_ts, f_low, label = 'Low')
plt.title('Real Estate High vs. Low')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(f_ts, f_tcs, label = 'Confirmed Cases')
plt.plot(f_ts, f_tds, label = 'Deaths')
plt.plot(f_ts, f_high, label = 'High')
plt.plot(f_ts, f_low, label = 'Low')
plt.title('Overall Real Estate Data')
plt.xlabel('Timeline')
plt.ylabel('Frequency')
plt.legend()
plt.show()