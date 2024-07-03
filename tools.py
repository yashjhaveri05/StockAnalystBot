import yfinance as yf
from langchain.tools import tool
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
        string = []
        for key, val in data.items():
            string.append(f"\n {key} : {val}")
        return "".join(string)

    @tool("Get 5 year historical data")
    def get_data(self):
        """Useful to retrieve the daily historical data for the last 5 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date"""
        return self.stock.history(period='5y').to_string()
    
    @tool("Get shareholders information")
    def get_shareholders(self):
        """Useful to retrieve shareholders in the comapny and categorize them. Returns the 
        major holders, institutional holders, and mutualfund holders and also return information 
        about insider transactions, insider purchases and insider roster holders."""
        shareholders = {}
        shareholders['major_holders'] = self.stock.major_holders
        shareholders['institutional_holders'] = self.stock.institutional_holders
        shareholders['mutualfund_holders'] = self.stock.mutualfund_holders
        shareholders['insider_transactions'] = self.stock.insider_transactions
        shareholders['insider_purchases'] = self.stock.insider_purchases
        shareholders['insider_roster_holders'] = self.stock.insider_roster_holders
        string = []
        for key, val in shareholders.items():
            string.append('\n'.join([f"{key}", f"{str(val)}", "\n-----------------\n"]))
        return "".join(string)
    
    @tool("Get company financial data")
    def get_financials(self):
        """Useful to retrieve financials of a company or stock and returns the 
        financials, income statement, balance sheet and cashflow"""
        financials = {}
        financials['financials'] = self.stock.financials
        financials['income_stmt'] = self.stock.income_stmt
        financials['quarterly_income_stmt'] = self.stock.quarterly_income_stmt
        financials['balance_sheet'] = self.stock.balance_sheet
        financials['quarterly_balance_sheet'] = self.stock.quarterly_balance_sheet
        financials['cashflow'] = self.stock.cashflow
        financials['quarterly_cashflow'] = self.stock.quarterly_cashflow
        string = []
        for key, val in financials.items():
            string.append('\n'.join([f"{key}", f"{str(val)}", "\n-----------------\n"]))
        return "".join(string)

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
            data = response.json()
            return data

        if "." in self.ticker:
            return ""
        else:
            gdp_data = get_alpha_vantage_data("REAL_GDP")
            inflation_data = get_alpha_vantage_data("CPI")
            interest_rate_data = get_alpha_vantage_data("FEDERAL_FUNDS_RATE")
            macro_data = {
                "gdp": gdp_data,
                "inflation": inflation_data,
                "interest_rate": interest_rate_data,
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
        return self.stock.history(period='1y').to_string()

class NewsDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Company News")
    def get_news(self):
        """Useful to retrieve news about a company, stock or any other
        topic and return relevant results"""
        news = self.stock.news
        string = []

        for n in news:
            try:
                string.append('\n'.join([
                    f"Title: {n['title']}", f"Link: {n['link']}",
                    f"Publisher: {n['publisher']}", "\n-----------------"
                ]))
            except KeyError:
                next
        return '\n'.join(string)

class RecommendationDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Recommendation Trends")
    def get_recommendations(self):
        """Useful to retrieve recommendation trends about a company or stock
        and return relevant results"""
        stock_recommendation = {}
        stock_recommendation['recommendations'] = self.stock.recommendations.to_numpy()
        stock_recommendation['recommendations_summary'] = self.stock.recommendations_summary.to_numpy()
        stock_recommendation['upgrades_downgrades'] = self.stock.upgrades_downgrades.to_numpy()
        string = []
        for key, val in stock_recommendation.items():
            string.append('\n'.join([f"{key}", f"{val}", "\n-----------------\n"]))
        return "".join(string)

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