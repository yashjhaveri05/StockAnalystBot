import os
from dotenv import load_dotenv
load_dotenv()
import yfinance as yf
from crewai_tools import tool
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime

gemini_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

# Define tools
@tool("Get Options Data")
def get_options(ticker: str) -> str:
    """ Useful for retrieving puts and calls data of a stock and 
        returns the relevant results for analysis"""
    stock = yf.Ticker(ticker)
    options = {}
    expirations = stock.options
    count = 0
    for date in expirations:
        if count < 2:
            options[date] = stock.option_chain(date)
            count += 1
        else:
            break
    return str(options)

# Define agents
def options_analyst():
    return Agent(
        role='Advanced Options Analyst',
        goal="Investigate options data to offer insights into market expectations and potential movements. Analyze earnings forecasts and market trends to predict future stock performance.",
        backstory="A seasoned analyst with extensive experience in options markets, adept at interpreting complex data to forecast potential market shifts and opportunities.",
        verbose=True,
        tools=[
            get_options
        ],
        llm = llm
    )

# Define tasks
def options_analysis_task(ticker):
    return Task(
        description=f"Analyze options data for the specified stock {ticker} and provide insights on market expectations.",
        expected_output=f"A report on options data for {ticker}, including market expectations and potential movements.",
        agent=options_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def options_crew(ticker):
    crew = Crew(
        agents=[
            options_analyst()
        ],
        tasks=[
            options_analysis_task(ticker)
        ],
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "AAPL"
    report = options_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_options_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")