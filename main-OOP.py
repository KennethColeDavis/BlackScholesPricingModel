#Black-Scholes Pricing Model
#Author: Kenneth Cole Davis
#Date: Nov 29, 2024
#Purpose: Use data manipulation concepts to consolidate relevant information to the current call options on the market 
#from an object oriented programming aproach. Then using the data to calculate a fair value price using the Black-Scholes 
#Pricing model and comparing that to current market prices to turn a profit.


#Import libraries
import pandas as pd
from yahooquery import Ticker
from blackScholesCalcs import BS_Calcs
from dataCleaning import Cleanse

#Establish baseline variables and pull original data
ticker = "AAPL"
stock = Ticker(ticker)
options = pd.DataFrame(stock.option_chain)

#Filter to just options
options = options.reset_index()
options = options[options['optionType'] == 'calls']

#Store and sort data
calls = Cleanse(options)

#Data cleaning and filtering
calls.MidPriceFilter()
calls.removeColumns()
calls.ReorderAndRename()

#Calculate Blacks-Scholes fair value, calculate difference, and input results 
BsCalls = BS_Calcs(calls.Dataframe, ticker)
BsCalls.BS_Implementation()

#Rounding and Dataframe assignemnt
FinalDf = Cleanse(BsCalls.DataFrame)
FinalDf.Round()
output = FinalDf.Dataframe

#Print and export results
file_name = f'Current{ticker}CallOptions.csv'
print(output)
output.to_csv(file_name, index=False)