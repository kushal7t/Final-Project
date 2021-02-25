####pip install alpha-vantage-pip install requests-pip install beautifulsoup4
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from pandas_datareader import data, wb
from datetime import date
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import requests
from bs4 import BeautifulSoup

confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse _covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed _global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse _covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_glo bal.csv"

###**my AlphaVantage key = KZPT32AEEXXIV6Y2**