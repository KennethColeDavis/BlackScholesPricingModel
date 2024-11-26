#Black-Scholes Pricing Model
#Author: Kenneth Cole Davis
#Date: Nov 25, 2024
#Purpose: Use the Black-Scholes pricing model to calculate a fair value and compare that value with market prices. 
#Then using this information and all other relevant information to export in the form of a csv file.

#Import libraries
from yahooquery import Ticker
import pandas as pd
from scipy.stats import norm
import numpy as np
from datetime import datetime

#Establish baseline variables
stock = "AAPL"
risk_free_rate = 0.045
ticker = Ticker(stock)

#Calculate cumulative distribution function for a standard normal distribution 
def N(x):
    return norm.cdf(x)

#Calculate days until expiration
def DatesDifference(expiration_Date):
    expiration_DateStr = str(expiration_Date)
    expiration_Date = datetime.strptime(expiration_DateStr, "%Y-%m-%d %H:%M:%S")
    current_Date = datetime.now()
    difference = (expiration_Date - current_Date)
    return difference.days

#Black-Scholes call options calculations 
def black_scholes_call (S, K, T, r, sigma, q):
    d1 = (np.log(S/K)+(r - q + sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    Call =  S * (np.exp(-q * T) * norm.cdf(d1)) - (norm.cdf(d2) * K * np.exp(-r * T))
    return Call

#Pull current dividend yeild and price
Fdata = ticker.financial_data[stock]
Sdata = ticker.summary_detail[stock]
current_price = Fdata["currentPrice"]
dividend_yeild = Sdata["dividendYield"]

#Pull options chain and filter to just options
options = ticker.option_chain
options_df = options.reset_index()
calls_df = options_df[options_df['optionType'] == 'calls']

#Calculate and filter out midprice
calls_df['mid_price'] = (calls_df['bid'] + calls_df['ask'])/2
calls_df = calls_df[calls_df['mid_price']>1]

#Calculate Black Scholes Value and input days, BS calcs, and price difference into DataFrame     
for index, row in calls_df.iterrows():
    days = DatesDifference(row['expiration'])
    calls_df.loc[index, 'daysToExpiration'] = days
    calls_df.loc[index, 'black_scholes_value'] = black_scholes_call(current_price, row['strike'],(days/365),
                         risk_free_rate, row['impliedVolatility'], dividend_yeild
                        )
    calls_df.loc[index, 'difference_in_price'] = (calls_df.loc[index, 'mid_price'] - calls_df.loc[index, 'black_scholes_value'])

#Clean up DataFrame
remove = ['optionType', 'currency', 'lastPrice', 'change',
             'percentChange','volume', 'openInterest', 'contractSize', 
             'lastTradeDate','inTheMoney'
        ]
keep = ['symbol', 'contractSymbol', 'expiration', 'daysToExpiration', 
        'strike', 'impliedVolatility', 'bid', 'ask', 'mid_price',
        'black_scholes_value', 'difference_in_price']

#Removing unnecessary columns
count = 0
while count < len(remove):   
    del calls_df[remove[count]]
    count += 1    

#Re-order and rename
calls_df = calls_df.reindex(columns = keep)            
calls_df = calls_df.rename(columns={"symbol": "stock"})  

#Rounding
calls_df['impliedVolatility'] = calls_df['impliedVolatility'].round(10)
calls_df['black_scholes_value'] = calls_df['black_scholes_value'].round(6)
calls_df['difference_in_price'] = calls_df['difference_in_price'].round(9)
calls_df['mid_price'] = calls_df['mid_price'].round(3)

#Name file and re-order indices
file_name = f'Current{stock}CallOptions.csv'
calls_df.reset_index(inplace=True, drop=True)  #Not necesarry but logical for possible future modification and print to terminal 

#Print to terminal and export CSV without indices
print(calls_df)
calls_df.to_csv(file_name, index=False)