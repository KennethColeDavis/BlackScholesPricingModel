#Black-Scholes Calculatins
#Author: Kenneth Cole Davis
#Date: Nov 29, 2024
#Purpose: Create a class that can take in a pandas dataframe and a stock ticker to calculate all options
#Black-Scholes fair value price using mathematical and statistical calculations

#Import libraries
from yahooquery import Ticker
import pandas as pd
from scipy.stats import norm
import numpy as np
from datetime import datetime

class BS_Calcs:
    #Constructor
    def __init__ (self, Data: pd.DataFrame, ticker):
        self.DataFrame = Data
        self.ticker = ticker
        self.stock = Ticker(ticker)
        self.risk_free_rate = .045

    #Pull current price of for a given stock
    def currentPrice(self):
        Fdata = self.stock.financial_data[self.ticker]
        current_price = Fdata["currentPrice"]
        return current_price

    #Pull dividend yeild value for a given stock
    def dividendYeild(self):
        Sdata = self.stock.summary_detail[self.ticker]
        dividend_yeild = Sdata["dividendYield"]
        return dividend_yeild
    
    #Calculate the amount of whole days between now and the call options contract experation date
    def DatesDifference(self,expiration_Date):
        expiration_DateStr = str(expiration_Date)
        expiration_Date = datetime.strptime(expiration_DateStr, "%Y-%m-%d %H:%M:%S")
        current_Date = datetime.now()
        difference = (expiration_Date - current_Date)
        return difference.days
    
    #Calculate the BS pricing model value of a singular call option contract.
    def BS_Value (self, S, K, T, r, sigma, q):
        d1 = (np.log(S/K)+(r - q + sigma**2/2)*T) / (sigma * np.sqrt(T))
        d2 = d1 - (sigma * np.sqrt(T))
        Call =  S * (np.exp(-q * T) * norm.cdf(d1)) - (norm.cdf(d2) * K * np.exp(-r * T))
        return Call
    
    #Loop function to input the BS value and difference in market price for each call option contract.
    def BS_Implementation(self):
        CP = self.currentPrice()
        DY = self.dividendYeild()
        for index, row in self.DataFrame.iterrows():
            now = row['expiration']
            days = self.DatesDifference(now)
            self.DataFrame.loc[index, 'daysToExpiration'] = int(round(days, 0))
            self.DataFrame.loc[index, 'black_scholes_value'] = self.BS_Value(CP, row['strike'],(days/365),
                         self.risk_free_rate, row['impliedVolatility'], DY
                        )
            self.DataFrame.loc[index, 'difference_in_price'] = (self.DataFrame.loc[index, 'mid_price'] - self.DataFrame.loc[index, 'black_scholes_value'])


    #Helper to calculate the cumulative distribution for a standard normal distribution 
    @staticmethod
    def N(x):
        return norm.cdf(x)
    
