# BlackScholesPricingModel
This project demonstrates the application of the Black-Scholes model to calculate the fair value of call options for a selected stock. Using the yahooquery library, financial and options chain data is programmatically retrieved from Yahoo Finance's API. The model incorporates variables such as stock price, strike price, time to expiration, risk-free rate, volatility, and dividend yield to compute theoretical option values.

The calculated values are compared to mid-market prices, enabling the identification of price discrepancies. The project further processes and filters the options data to include key metrics like implied volatility, days to expiration, and pricing differences, which are organized in a clean DataFrame. Results are exported as a CSV file for further analysis, providing a structured dataset that can inform trading decisions or financial modeling.

This project combines advanced financial modeling, data manipulation using Python libraries such as pandas and numpy, and statistical calculations to bridge data science and quantitative finance.

The Object-Oriented approach I did can alos be found on my github
