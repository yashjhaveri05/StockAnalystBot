import yfinance as yf
from crewai_tools import tool
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class FundamentalDataTool:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    @tool("Get Company Fundamentals")
    def get_fundamentals(self):
        """Useful to retrieve basic information about a company or stock and return
        relevant results aligning towards the fundamental aspects of the company"""
        data = self.stock.info
        if not data:
            return "No fundamental data available."
        string = []
        for key, val in data.items():
            string.append(f"\n {key} : {val}")
        return "".join(string)

    @tool("Get 5 year historical data")
    def get_data(self):
        """Useful to retrieve the daily historical data for the last 5 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date"""
        data = self.stock.history(period='5y')
        if data.empty:
            return "No historical data available."
        return data.to_string()
    
    @tool("Get shareholders information")
    def get_shareholders(self):
        """Useful to retrieve shareholders in the comapny and categorize them. Returns the 
        major holders, institutional holders, and mutualfund holders and also return information 
        about insider transactions, insider purchases and insider roster holders."""
        shareholders = {
            'major_holders': self.stock.major_holders,
            'institutional_holders': self.stock.institutional_holders,
            'mutualfund_holders': self.stock.mutualfund_holders,
            'insider_transactions': self.stock.insider_transactions,
            'insider_purchases': self.stock.insider_purchases,
            'insider_roster_holders': self.stock.insider_roster_holders
        }
        return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in shareholders.items() if val is not None])
    
    @tool("Get company financial data")
    def get_financials(self):
        """Useful to retrieve financials of a company or stock and returns the 
        financials, income statement, balance sheet and cashflow"""
        financials = {
            'financials': self.stock.financials,
            'income_stmt': self.stock.income_stmt,
            'quarterly_income_stmt': self.stock.quarterly_income_stmt,
            'balance_sheet': self.stock.balance_sheet,
            'quarterly_balance_sheet': self.stock.quarterly_balance_sheet,
            'cashflow': self.stock.cashflow,
            'quarterly_cashflow': self.stock.quarterly_cashflow
        }
        return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in financials.items() if val is not None])

class MacroEconomicDataTool:
    def __init__(self, ticker):
        self.ticker = ticker
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

    @tool("Get macro Economic Data")
    def get_macro_economic(self):
        """Useful to retrieve macro economic indicators and returns 
        gdp data, inflation data and interest rate data."""
        def get_alpha_vantage_data(function):
            url = f"https://www.alphavantage.co/query?function={function}&apikey={self.api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}

        if "." in self.ticker:
            return "Invalid ticker for macroeconomic data."
        macro_data = {
            "gdp": get_alpha_vantage_data("REAL_GDP"),
            "inflation": get_alpha_vantage_data("CPI"),
            "interest_rate": get_alpha_vantage_data("FEDERAL_FUNDS_RATE")
        }
        return str(macro_data)

class TechnicalDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get 1 year historical data")
    def get_data(self):
        """Useful to retrieve the daily historical data for the last 1 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date. This data can be used for 
        charting, technical analysis and calculating technical indicators."""
        data = self.stock.history(period='1y')
        if data.empty:
            return "No historical data available."
        return data.to_string()

class NewsDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Company News")
    def get_news(self):
        """Useful to retrieve news about a company, stock or any other
        topic and return relevant results"""
        news = self.stock.news
        if not news:
            return "No news available."
        return "\n-----------------\n".join([
            f"Title: {n.get('title')}\nLink: {n.get('link')}\nPublisher: {n.get('publisher')}"
            for n in news
        ])
    
class RecommendationDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Recommendation Trends")
    def get_recommendations(self):
        """Useful to retrieve recommendation trends about a company or stock
        and return relevant results"""
        stock_recommendation = {
            'recommendations': self.stock.recommendations.to_numpy(),
            'recommendations_summary': self.stock.recommendations_summary.to_numpy(),
            'upgrades_downgrades': self.stock.upgrades_downgrades.to_numpy()
        }
        return "\n-----------------\n".join([
            f"{key}\n{val}" for key, val in stock_recommendation.items() if val is not None
        ])

class FutureOptionsDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Futures Data")
    def get_futures(self):
        """ Fetches EPS Estimate, Reported EPS and Surprise % for the earnings data
        and returns this information"""
        return self.stock.get_earnings_dates(limit=20).to_string()
    
    @tool("Get Options Data")
    def get_options(self):
        """ Useful for retrieving puts and calls data of a stock and 
        returns the relevant results for analysis"""
        options = {}
        expirations = self.stock.options
        count = 0
        for date in expirations:
            if count < 5:
                options[date] = self.stock.option_chain(date)
                count+=1
            else:
                break
        return str(options)