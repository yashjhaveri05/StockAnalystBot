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
        string.append(f"\n {key} : {val}")
    return "".join(string)

@tool("Get 5 year historical data")
def get_5_year_historical_data(ticker: str) -> str:
    """Useful to retrieve the daily historical data for the last 5 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date"""
    stock = yf.Ticker(ticker)
    data = stock.history(period='5y')
    if data.empty:
        return "No historical data available."
    return data.to_string()

@tool("Get shareholders information")
def get_shareholders(ticker: str) -> str:
    """Useful to retrieve shareholders in the comapny and categorize them. Returns the 
        major holders, institutional holders, and mutualfund holders and also return information 
        about insider transactions, insider purchases and insider roster holders."""
    stock = yf.Ticker(ticker)
    shareholders = {
        'major_holders': stock.major_holders,
        'institutional_holders': stock.institutional_holders,
        'mutualfund_holders': stock.mutualfund_holders,
        'insider_transactions': stock.insider_transactions,
        'insider_purchases': stock.insider_purchases,
        'insider_roster_holders': stock.insider_roster_holders
    }
    return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in shareholders.items() if val is not None])

@tool("Get company financial data")
def get_financials(ticker: str) -> str:
    """Useful to retrieve financials of a company or stock and returns the 
        financials, income statement, balance sheet and cashflow"""
    stock = yf.Ticker(ticker)
    financials = {
        'financials': stock.financials,
        'income_stmt': stock.income_stmt,
        'quarterly_income_stmt': stock.quarterly_income_stmt,
        'balance_sheet': stock.balance_sheet,
        'quarterly_balance_sheet': stock.quarterly_balance_sheet,
        'cashflow': stock.cashflow,
        'quarterly_cashflow': stock.quarterly_cashflow
    }
    return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in financials.items() if val is not None])

@tool("Get macro Economic Data")
def get_macro_economic(ticker: str) -> str:
    """Useful to retrieve macro economic indicators and returns 
        gdp data, inflation data and interest rate data."""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

    def get_alpha_vantage_data(function):
        url = f"https://www.alphavantage.co/query?function={function}&apikey={api_key}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}

    if "." in ticker:
        return "Invalid ticker for macroeconomic data."
    macro_data = {
        "gdp": get_alpha_vantage_data("REAL_GDP"),
        "inflation": get_alpha_vantage_data("CPI"),
        "interest_rate": get_alpha_vantage_data("FEDERAL_FUNDS_RATE")
    }
    return str(macro_data)

@tool("Get 1 year historical data")
def get_1_year_historical_data(ticker: str) -> str:
    """Useful to retrieve the daily historical data for the last 1 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date. This data can be used for 
        charting, technical analysis and calculating technical indicators."""
    stock = yf.Ticker(ticker)
    data = stock.history(period='1y')
    if data.empty:
        return "No historical data available."
    return data.to_string()

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

@tool("Get Recommendation Trends")
def get_recommendations(ticker: str) -> str:
    """Useful to retrieve recommendation trends about a company or stock
        and return relevant results"""
    stock = yf.Ticker(ticker)
    stock_recommendation = {
        'recommendations': stock.recommendations.to_numpy(),
        'recommendations_summary': stock.recommendations_summary.to_numpy(),
        'upgrades_downgrades': stock.upgrades_downgrades.to_numpy()
    }
    return "\n-----------------\n".join([
        f"{key}\n{val}" for key, val in stock_recommendation.items() if val is not None
    ])

@tool("Get Futures Data")
def get_futures(ticker: str) -> str:
    """ Fetches EPS Estimate, Reported EPS and Surprise % for the earnings data
        and returns this information"""
    stock = yf.Ticker(ticker)
    return stock.get_earnings_dates(limit=20).to_string()

@tool("Get Options Data")
def get_options(ticker: str) -> str:
    """ Useful for retrieving puts and calls data of a stock and 
        returns the relevant results for analysis"""
    stock = yf.Ticker(ticker)
    options = {}
    expirations = stock.options
    count = 0
    for date in expirations:
        if count < 5:
            options[date] = stock.option_chain(date)
            count += 1
        else:
            break
    return str(options)

# Define agents
def fundamental_analyst():
    return Agent(
        role='Elite Fundamental Analyst',
        goal="Perform a meticulous analysis of the company's financial health, including historical data, dividend records, stock splits, share counts, major shareholders, financial statements, earnings reports, and forecasts. Provide investment recommendations by identifying undervalued stocks and predicting potential growth opportunities.",
        backstory="A highly experienced financial analyst renowned for in-depth fundamental analysis and strategic investment advice, committed to delivering exceptional insights for a high-profile client.",
        verbose=True,
        tools=[
            get_fundamentals,
            get_5_year_historical_data,
            get_shareholders,
            get_financials,
            get_macro_economic
        ],
        llm = llm
    )

def technical_analyst():
    return Agent(
        role='Master Technical Analyst and Chartist',
        goal="Examine and interpret the technical aspects of the stock, including chart patterns, trading volumes, and technical indicators. Identify trends and forecast future stock movements to provide actionable trading insights.",
        backstory="A technical analysis expert with a sharp eye for detail, specializing in chart patterns and technical indicators to predict market movements with precision.",
        verbose=True,
        tools=[
            get_1_year_historical_data
        ],
        llm = llm
    )

def news_sentiment_analyst():
    return Agent(
        role='Top News and Sentiment Analyst',
        goal="Evaluate the latest news and media coverage related to the stock. Assess overall market sentiment and its potential impact on stock performance, providing insights into market dynamics and investor behavior.",
        backstory="A market sentiment specialist with a deep understanding of news analysis, skilled in gauging the impact of media coverage on stock performance and investor attitudes.",
        verbose=True,
        tools=[
            get_news
        ],
        llm = llm
    )

def recommendation_analyst():
    return Agent(
        role='Premier Recommendation Analyst',
        goal="Analyze and summarize analyst recommendations and market outlooks for the specified stock. Provide a comprehensive summary of sentiments from various market experts.",
        backstory="An expert in synthesizing analyst opinions, known for delivering clear and concise summaries of market sentiments and recommendations from top financial experts.",
        verbose=True,
        tools=[
            get_recommendations
        ],
        llm = llm
    )

def future_options_analyst():
    return Agent(
        role='Advanced Futures and Options Analyst',
        goal="Investigate futures and options data to offer insights into market expectations and potential movements. Analyze earnings forecasts and market trends to predict future stock performance.",
        backstory="A seasoned analyst with extensive experience in futures and options markets, adept at interpreting complex data to forecast potential market shifts and opportunities.",
        verbose=True,
        tools=[
            get_futures,
            get_options
        ],
        llm = llm
    )

def financial_analyst():
    return Agent(
        role='Chief Financial Analyst',
        goal="Deliver comprehensive financial insights and market trend analysis to impress high-profile clients. Combine macroeconomic data, fundamental and technical analysis, news sentiment, and recommendations to provide holistic investment advice.",
        backstory="A distinguished financial analyst with a broad skill set encompassing various aspects of market analysis, dedicated to providing unparalleled investment recommendations for prestigious clients.",
        verbose=True,
        tools=[
            get_macro_economic,
            get_fundamentals,
            get_5_year_historical_data,
            get_shareholders,
            get_financials,
            get_news,
            get_recommendations,
        ],
        allow_delegation=True,
        llm = llm
    )

def research_analyst():
    return Agent(
        role='Leading Research Analyst',
        goal="Gather, interpret, and present data effectively to astound clients with comprehensive research reports. Analyze fundamental data, news sentiment, and recommendations to deliver insightful findings.",
        backstory="Recognized as the top research analyst, renowned for exceptional skills in data interpretation and report generation, currently engaged with an important client to deliver outstanding research insights.",
        verbose=True,
        tools=[
            get_fundamentals,
            get_5_year_historical_data,
            get_shareholders,
            get_financials,
            get_news,
            get_recommendations
        ],
        llm = llm
    )

def investor_advisor():
    return Agent(
        role='Senior Investment Advisor',
        goal="Provide full-spectrum stock analysis and investment recommendations to impress high-profile clients. Integrate macroeconomic trends, fundamental and technical analysis, news sentiment, recommendations, and options data to formulate strategic advice.",
        backstory="An experienced investment advisor with a proven track record of combining diverse analytical insights to craft strategic investment plans, dedicated to impressing top-tier clients.",
        verbose=True,
        tools=[
            get_macro_economic,
            get_fundamentals,
            get_5_year_historical_data,
            get_shareholders,
            get_financials,
            get_1_year_historical_data,
            get_news,
            get_recommendations,
            get_futures,
            get_options
        ],
        allow_delegation=True,
        llm = llm
    )

def report_writer():
    return Agent(
        role='Expert Financial Report Writer',
        goal="Compile detailed and coherent reports based on all the comprehensive stock analysis. Synthesize data from various analyses into a well-structured document for stakeholders.",
        backstory="An accomplished report writer with extensive experience in transforming complex data into clear, informative reports, adept at delivering high-quality documentation for stakeholders.",
        verbose=True,
        tools=[
            get_macro_economic,
            get_fundamentals,
            get_5_year_historical_data,
            get_shareholders,
            get_financials,
            get_1_year_historical_data,
            get_news,
            get_recommendations,
            get_futures,
            get_options
        ],
        llm = llm
    )

# Define tasks
def fundamental_analysis_task(ticker):
    return Task(
        description=f"Analyze the fundamental data of the company {ticker} and provide a comprehensive report. Include company information, historical data, dividend and stock split timeline, share count, top shareholders, financial statements, earnings and earning forecast, price target, market trends, economic factors, and sustainability.",
        expected_output=f"A detailed report on {ticker} including all fundamental analysis aspects. The report should provide clear investment recommendations.",
        agent=fundamental_analyst()
    )

def technical_analysis_task(ticker):
    return Task(
        description=f"Analyze the technical data of the specified stock {ticker} and identify key trends, patterns, and technical indicators.",
        expected_output=f"A technical analysis report on {ticker} highlighting key trends, patterns, and indicators.",
        agent=technical_analyst()
    )

def news_analysis_task(ticker):
    return Task(
        description=f"Analyze the latest news related to the specified stock {ticker} and assess the overall sentiment.",
        expected_output=f"A sentiment analysis report on {ticker} based on the latest news articles and media coverage.",
        agent=news_sentiment_analyst()
    )

def recommendation_analysis_task(ticker):
    return Task(
        description=f"Analyze analyst recommendations and provide a summary of their sentiment towards the specified stock {ticker}.",
        expected_output=f"A summary report of analyst recommendations and market outlooks for {ticker}.",
        agent=recommendation_analyst()
    )

def future_options_analysis_task(ticker):
    return Task(
        description=f"Analyze futures and options data for the specified stock {ticker} and provide insights on market expectations.",
        expected_output=f"A report on futures and options data for {ticker}, including market expectations and potential movements.",
        agent=future_options_analyst()
    )

def financial_analysis_task(ticker):
    return Task(
        description=f"Conduct a comprehensive financial analysis of {ticker}, including macroeconomic data, fundamental data, news sentiment, analyst recommendations, and futures and options data.",
        expected_output=f"A detailed financial analysis report on {ticker}, encompassing all aspects of macroeconomic, fundamental, news, recommendations, and futures/options data.",
        agent=financial_analyst(),
        dependencies=[
            fundamental_analysis_task(ticker),
            news_analysis_task(ticker),
            recommendation_analysis_task(ticker)
        ]
    )

def research_task(ticker):
    return Task(
        description=f"Gather and interpret data related to {ticker} and provide a comprehensive report. Include fundamental data, news sentiment, and analyst recommendations.",
        expected_output=f"A detailed research report on {ticker}, including fundamental data, news sentiment, and analyst recommendations.",
        agent=research_analyst()
    )

def investment_advice_task(ticker):
    return Task(
        description=f"Provide a comprehensive investment recommendation for {ticker}, combining macroeconomic data, fundamental data, technical analysis, news sentiment, analyst recommendations, and futures/options data.",
        expected_output=f"A detailed investment recommendation report for {ticker}, incorporating insights from all relevant data sources.",
        agent=investor_advisor(),
        dependencies=[
            technical_analysis_task(ticker),
            future_options_analysis_task(ticker),
            financial_analysis_task(ticker),
            research_task(ticker)
        ]
    )

def report_writing_task(ticker):
    return Task(
        description=f"Compile a detailed report based on the comprehensive analysis of the specified stock {ticker}.",
        expected_output=f"A comprehensive financial report on {ticker}, synthesizing data from various analyses into a coherent document.",
        agent=report_writer(),
        dependencies=[
            technical_analysis_task(ticker),
            future_options_analysis_task(ticker),
            financial_analysis_task(ticker),
            research_task(ticker),
            investment_advice_task(ticker)
        ]
    )

# Form the crew and kickoff with user-provided stock input
def form_and_kickoff_crew(ticker):
    crew = Crew(
        agents=[
            fundamental_analyst(),
            technical_analyst(),
            news_sentiment_analyst(),
            recommendation_analyst(),
            future_options_analyst(),
            financial_analyst(),
            research_analyst(),
            investor_advisor(),
            report_writer()
        ],
        tasks=[
            fundamental_analysis_task(ticker),
            technical_analysis_task(ticker),
            news_analysis_task(ticker),
            recommendation_analysis_task(ticker),
            future_options_analysis_task(ticker),
            financial_analysis_task(ticker),
            research_task(ticker),
            investment_advice_task(ticker),
            report_writing_task(ticker)
        ],
        process=Process.sequential
    )
    
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "AAPL"
    report = form_and_kickoff_crew(stock_ticker)
    print(report)