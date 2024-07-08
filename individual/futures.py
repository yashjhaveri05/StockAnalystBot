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
@tool("Get Futures Data")
def get_futures(ticker: str) -> str:
    """ Fetches EPS Estimate, Reported EPS and Surprise % for the earnings data
        and returns this information"""
    stock = yf.Ticker(ticker)
    return stock.get_earnings_dates(limit=20).to_string()

# Define agents
def future_analyst():
    return Agent(
        role='Advanced Futures Analyst',
        goal="Investigate futures data to offer insights into market expectations and potential movements. Analyze earnings forecasts and market trends to predict future stock performance.",
        backstory="A seasoned analyst with extensive experience in futures markets, adept at interpreting complex data to forecast potential market shifts and opportunities.",
        verbose=True,
        tools=[
            get_futures
        ],
        llm = llm
    )

# Define tasks
def future_analysis_task(ticker):
    return Task(
        description=f"Analyze futures data for the specified stock {ticker} and provide insights on market expectations.",
        expected_output=f"A report on futures data for {ticker}, including market expectations and potential movements.",
        agent=future_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def futures_crew(ticker):
    crew = Crew(
        agents=[
            future_analyst()
        ],
        tasks=[
            future_analysis_task(ticker)
        ],
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "AAPL"
    report = futures_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_futures_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")