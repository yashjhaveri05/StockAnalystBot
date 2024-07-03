import yfinance as yf
import pandas as pd
import requests

def get_financial_data(ticker, alpha_vantage_key):
    stock = yf.Ticker(ticker)

    # Fetch basic info
    info = stock.info
    
    # Fetch historical market data
    hist = stock.history(period="5y")
    
    # Fetch financial statements
    financials = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cash_flow = stock.cashflow.T
    
    # Fetch earnings history
    earnings = stock.earnings.T

    # Fetch analyst recommendations and price target
    recommendations = stock.recommendations
    price_target = stock.analyst_price_target
    earnings_estimates = stock.earnings_forecasts

    # Fetch sustainability data
    sustainability = stock.sustainability

    # Fetch macroeconomic data using Alpha Vantage
    def get_alpha_vantage_data(function):
        url = f"https://www.alphavantage.co/query?function={function}&apikey={alpha_vantage_key}"
        response = requests.get(url)
        data = response.json()
        return data

    # Example macro data
    gdp_data = get_alpha_vantage_data("REAL_GDP")
    inflation_data = get_alpha_vantage_data("CPI")
    interest_rate_data = get_alpha_vantage_data("FEDERAL_FUNDS_RATE")

    macro_data = {
        "gdp": gdp_data,
        "inflation": inflation_data,
        "interest_rate": interest_rate_data,
    }

    # Create a dictionary to store all the data
    data = {
        "info": info,
        "historical_data": hist,
        "financials": financials,
        "balance_sheet": balance_sheet,
        "cash_flow": cash_flow,
        "earnings": earnings,
        "recommendations": recommendations,
        "price_target": price_target,
        "earnings_estimates": earnings_estimates,
        "sustainability": sustainability,
        "macro_data": macro_data
    }
    
    return data

# Example usage
ticker = 'AAPL'  # Replace with the desired stock ticker
alpha_vantage_key = 'your_alpha_vantage_api_key'  # Replace with your Alpha Vantage API key

financial_data = get_financial_data(ticker, alpha_vantage_key)

# Display the financial data
for key, value in financial_data.items():
    if isinstance(value, pd.DataFrame):
        print(f"\n{key}:\n", value)
    else:
        print(f"\n{key}:\n", value)

# Save financial data to CSV files
financial_data["historical_data"].to_csv(f'{ticker}_historical_data.csv')
financial_data["financials"].to_csv(f'{ticker}_financials.csv')
financial_data["balance_sheet"].to_csv(f'{ticker}_balance_sheet.csv')
financial_data["cash_flow"].to_csv(f'{ticker}_cash_flow.csv')
financial_data["earnings"].to_csv(f'{ticker}_earnings.csv')
if financial_data["recommendations"] is not None:
    financial_data["recommendations"].to_csv(f'{ticker}_recommendations.csv')
if financial_data["price_target"] is not None:
    financial_data["price_target"].to_csv(f'{ticker}_price_target.csv')
if financial_data["earnings_estimates"] is not None:
    financial_data["earnings_estimates"].to_csv(f'{ticker}_earnings_estimates.csv')
if financial_data["sustainability"] is not None:
    financial_data["sustainability"].to_csv(f'{ticker}_sustainability.csv')
