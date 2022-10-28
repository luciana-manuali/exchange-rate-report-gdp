import pandas as pd
from datetime import datetime

exchange_rates_info = r'C:\Users\jsaul\Dropbox\gdp-trabajos-lucianamanuali\Data\Exchange Rate\Exchange Rate.xlsm'

exchange_rates = pd.read_excel(exchange_rates_info, sheet_name = 'ER', usecols = 'A,B,C,D,E', engine='openpyxl')
exchange_rates = exchange_rates.set_index('Date')
exchange_rates.to_csv('exchange_rates.csv', index=True)

real_exchange_rates = pd.read_excel('http://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/ITCRMSerie.xls', header = 1, index_col = 0,usecols = 'A,B,C,F').dropna().iloc[800:]
new_dates = []
for excel_date in real_exchange_rates.index:
    date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
    new_dates.append(date)
real_exchange_rates.index = new_dates
real_exchange_rates.index.names = ['Date']
real_exchange_rates.to_csv('real_exchange_rates.csv', index=True)