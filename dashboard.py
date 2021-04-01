import streamlit as st 
import pandas as pd 
import numpy as np 
import requests

import yfinance as yf
import os
import datetime 
from Pattern_Finder_Func import is_consolidating
import plotly.graph_objects as go


# st.title("This is the title")

# st.header("This is a header")

# st.subheader('Subheader')

# st.write('This is regular text')

# '''
# # header
# ## subheader
# '''



# some_dictionary = {
#     'key' : 'value',
#     'key2' : 'value2'
# }

# some_list = [1,2,3]
# st.write(some_dictionary)
# st.write(some_list)
updated_time = 0
st.sidebar.write('''# Stock Data Dashboard''' )
option = st.sidebar.selectbox('''# Which dashbaord?''', ('Stock Chart','Consolidating stock finder','Stock Twits','pattern'))
# start_date = st.sidebar.slider("Stock data starting date", value = date(1990,1,1), format= "MM/DD/YYYY ")






st.header(option)

if option == 'Stock Twits':

    symbol = st.sidebar.text_input('Ticker', value='AAPL', max_chars=5)

    st.subheader("stocktwits")

    r= requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if option == 'Stock Chart':

    date_range = st.sidebar.date_input("Date range input", [datetime.date(2015, 1, 1) , datetime.date.today()] )
    # st.write("""
    # # Simple Stock Price App
    # """)
    tickerSymbol = st.sidebar.text_input('Ticker', value='AAPL', max_chars=5)
    # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
    #define the ticker symbol
    #get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)
    #get the historical prices for this ticker
   
    tickerDf = tickerData.history(period='1d', start=date_range[0], end=date_range[1])
    # Open	High	Low	Close	Volume	Dividends	Stock Splits
    
    st.write('''
    Closing Price
    ''')

    st.line_chart(tickerDf.Close)

    st.write('''
    Volume
    ''')
    st.line_chart(tickerDf.Volume)

    st.write('''
    Data Table
    ''')
    st.write(tickerDf)
    
    
    st.write('''
    Candlestick Graph
    ''')
    candlestick = go.Candlestick(x = tickerDf.index, open = tickerDf['Open'],high=tickerDf['High'], low = tickerDf['Low'], close=tickerDf['Close'])
    shapes = [

        dict(x0='2019-05-05', x1='2019-05-05', y0=0, y1=1, xref='x', yref='paper'),
        dict(x0='2019-07-30', x1='2019-07-30', y0=0, y1=1, xref='x', yref='paper'),

    ]
    annotations=[

        dict(x='2019-05-05', y=0.5, xref='x', yref='paper', showarrow=False, xanchor='left', text='Trump Tariff Tweet'),
        dict(x='2019-07-30', y=0.3, xref='x', yref='paper', showarrow=False, xanchor='left', text='Trump Tweets "China is doing very badly"'),
        
    ]
    figure = go.Figure(data=[candlestick])
    # figure.update_layout(annotations=annotations, shapes=shapes)
    figure.layout.xaxis.type = 'category' ## to remove blank dates. Weekends show up as blank becuase the stock market is closed on weekends.
    figure.update_layout(height = 800, width =1000)
    st.plotly_chart(figure)


if option == 'Consolidating stock finder':
    update_result = st.sidebar.button('Update S&P 500 Data')
    if update_result == True:   
        sp500_list = pd.read_csv(r'.\datasets\symbols.csv', names = ['abb','full name']) # Importing the CSV file with no header.
        test_list = sp500_list.head(10)

        for abb in sp500_list['abb']:
            # st.write(abb)
            data = yf.download(abb)
            data.to_csv('datasets/daily/{}.csv'.format(abb))
            updated_time= datetime.date.today() # Currently the updated time does not get stored permanantly 
        st.write('updated!!')
        # st.write(sp500_list) # Create a show and hide button.
    
    
    st.write(''' Looks for companies that are consolidating using the closing stock price.        ''')
    find_consolidated_result = st.button('''
    Find consolidating companies!      
    ''')
    stock_price_percent_range = st.number_input('Stock price movement range in %',min_value=1, max_value=100, value =3 )
    stock_price_date_range = st.number_input('Stock price date range', value = 15)
    if find_consolidated_result == True:
        for filename in os.listdir('datasets/daily'):
 
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            
            if is_consolidating(df, stock_price_percent_range,stock_price_date_range ):
                # st.image(r'https://stockcharts.com/c-sc/sc?s={}&p=D&b=5&g=0&i=0&r=1617234698402'.format(filename.split('.')[0]))
                st.write("{} is consolidating".format(filename.split('.')[0]))
                st.image(r'https://finviz.com/chart.ashx?t={}'.format(filename.split('.')[0]))

            # if is_breaking_out(df, percentage = stock_price_percent_range):
            #     print("{} is breaking out".format(filename))
            


    # find_consolidated_result2 = st.button('ticker for single testing')
    # stock_price_ticker2 = st.text_input('ticker', 'aapl')
    # stock_price_percent_range2 = st.number_input('Single Stock price % range', 2)
    # if find_consolidated_result2 == True:
    #     df = pd.read_csv('datasets/daily/{}'.format(stock_price_ticker2))
    
    #     if is_consolidating(df, stock_price_percent_range ):
    #         st.write("{} is consolidating".format(stock_price_ticker2))

    # # if is_breaking_out(df, percentage = stock_price_percent_range):
    # #     print("{} is breaking out".format(filename))



