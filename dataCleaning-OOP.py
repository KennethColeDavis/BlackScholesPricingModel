#Black-Scholes Pricing Model
#Author: Kenneth Cole Davis
#Date: Nov 29, 2024
#Purpose: Create a class that can take in a Pandas data frame from Yahooquery to sort, clean and manipulate 
#the dataframe to consolidate relevant information.

#Import libraries
import pandas as pd

class Cleanse:
    #Constructor
    def __init__(self,Data: pd.DataFrame):
        self.Dataframe = Data
        self.Remove = ['optionType', 'currency', 'lastPrice', 'change',
             'percentChange','volume', 'openInterest', 'contractSize', 
             'lastTradeDate','inTheMoney']
        self.Keep = ['symbol', 'contractSymbol', 'expiration', 'daysToExpiration', 
        'strike', 'impliedVolatility', 'bid', 'ask', 'mid_price',
        'black_scholes_value', 'difference_in_price']
        
    #Calculate and filter out options with a mid-price less than one
    def MidPriceFilter(self):
        #Calculate and filter out midprice
        self.Dataframe['mid_price'] = (self.Dataframe['bid'] + self.Dataframe['ask'])/2
        self.Dataframe = self.Dataframe[self.Dataframe['mid_price']>1]

    #Remove columns holding irrelevant information
    def removeColumns(self):
        count = 0
        while count < len(self.Remove):   
            del self.Dataframe[self.Remove[count]]
            count += 1 

    #Reorder and Rename columns for relevancys and clarity
    def ReorderAndRename(self):
        self.Dataframe = self.Dataframe.reindex(columns = self.Keep)            
        self.Dataframe = self.Dataframe.rename(columns={"symbol": "stock"})
        self.Dataframe.reset_index(inplace=True, drop=True)  

    #Round columns with more precision than necessary
    def Round(self):
        self.Dataframe['impliedVolatility'] = self.Dataframe['impliedVolatility'].round(10)
        self.Dataframe['black_scholes_value'] = self.Dataframe['black_scholes_value'].round(6)
        self.Dataframe['difference_in_price'] = self.Dataframe['difference_in_price'].round(9)
        self.Dataframe['mid_price'] = self.Dataframe['mid_price'].round(3) 





