import os
from dotenv import load_dotenv
import yfinance as yf
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

# Define tools
@tool("Get Company Fundamentals")
def get_fundamentals(ticker: str) -> str:
    """Useful to retrieve basic information about a company or stock and return
        relevant results aligning towards the fundamental aspects of the company"""
    stock = yf.Ticker(ticker)
    data = stock.info
    if not data:
        return "No fundamental data available."
    string = []
    for key, val in data.items():
        if key not in ['address1', 'city', 'state', 'zip', 'country', 'phone', 'website', 'longBusinessSummary', 'fullTimeEmployees', 'companyOfficers', 'exchange', 'quoteType', 'symbol', 'underlyingSymbol', 'shortName', 'longName', 'firstTradeDateEpochUtc', 'timeZoneFullName', 'timeZoneShortName', 'uuid', 'messageBoardId', 'gmtOffSetMilliseconds']:
            string.append(f"\n {key} : {val}")
    return "".join(string)

@tool("Get shareholders information")
def get_shareholders(ticker: str) -> str:
    """Useful to retrieve shareholders in the comapny and categorize them. Returns the 
        major holders, institutional holders, and mutualfund holders and also return information 
        about insider transactions, insider purchases and insider roster holders."""
    stock = yf.Ticker(ticker)
    shareholders = {
        'institutional_holders': stock.institutional_holders,
        'insider_transactions': stock.insider_transactions[['Shares', 'Value', 'Text', 'Insider', 'Start Date']]
    }
    return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in shareholders.items() if val is not None])

@tool("Get company financial data")
def get_financials(ticker: str) -> str:
    """Useful to retrieve financials of a company or stock and returns the 
        financials, income statement, balance sheet and cashflow"""
    stock = yf.Ticker(ticker)
    financials = {
        'financials': stock.financials.iloc[:, :2],
        'balance_sheet': stock.balance_sheet.iloc[:, :2],
        'cashflow': stock.cashflow.iloc[:, :2]
    }
    return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in financials.items() if val is not None])

@tool("Get Company News")
def get_news(ticker: str) -> str:
    """Useful to retrieve news about a company, stock or any other
        topic and return relevant results"""
    stock = yf.Ticker(ticker)
    news = stock.news
    if not news:
        return "No news available."
    return "\n-----------------\n".join([
        f"Title: {n.get('title')}\nLink: {n.get('link')}\nPublisher: {n.get('publisher')}"
        for n in news
    ])

# Define agents
def fundamental_analyst():
    return Agent(
        role='Elite Fundamental Analyst',
        goal="Perform a meticulous analysis of the company's financial health, including company data, major shareholders, financial statements, and news. Provide investment recommendations and a summary of the company fundamentals.",
        backstory="A highly experienced financial analyst renowned for in-depth fundamental analysis and strategic investment advice, committed to delivering exceptional insights for a high-profile client.",
        verbose=True,
        tools=[
            get_fundamentals,
            get_shareholders,
            get_financials,
            get_news
        ],
        llm = llm
    )

# Define tasks
def fundamental_analysis_task(ticker):
    return Task(
        description=f"Analyze the fundamental data of the company {ticker} and provide a comprehensive report. Include company information, historical data, dividend and stock split timeline, share count, top shareholders, financial statements, earnings and earning forecast, price target, market trends, economic factors, and sustainability.",
        expected_output=f"A detailed report on {ticker} including all fundamental analysis aspects. Also, include metrics like EPS, P/E Ratio, Dividend Yield, P/B Ratio, Debt-to-Equity Ratio, (ROE), (ROA), Operating Margin, Free Cash Flow, Current Ratio in the report. The report should provide clear investment recommendations.",
        agent=fundamental_analyst()
    )

# Form the crew and kickoff with user-provided stock input
def form_and_kickoff_crew(ticker):
    crew = Crew(
        agents=[
            fundamental_analyst(),
        ],
        tasks=[
            fundamental_analysis_task(ticker),
        ],
        process=Process.sequential
    )
    
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "AAPL"
    report = form_and_kickoff_crew(stock_ticker)
    print(report)