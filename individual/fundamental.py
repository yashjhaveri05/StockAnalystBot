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

# Define agents
def fundamental_analyst():
    return Agent(
        role='Elite Fundamental Analyst',
        goal="Perform a meticulous analysis of the company's financial health. Provide a summary of the company fundamentals and important fundamental metrics.",
        backstory="A highly experienced fundamental analyst renowned for in-depth fundamental analysis, committed to delivering exceptional insights for a high-profile client.",
        verbose=True,
        tools=[
            get_fundamentals
        ],
        llm = llm
    )

# Define tasks
def fundamental_analysis_task(ticker):
    return Task(
        description=f"Analyze the fundamental data of the company {ticker} and provide a comprehensive report. Include company information and important fundamental metrics in a well-organized format for simple reading by user. In the footnotes, also provide the description of these metrics.",
        expected_output=f"A detailed report on {ticker} including all fundamental analysis aspects. Also, include fundamental metrics in a well-organized format for simple reading by user. In the footnotes, also provide the description of these metrics.",
        agent=fundamental_analyst(),
    )

# Define crew
def fundamental_crew(ticker):
    crew = Crew(
        agents=[
            fundamental_analyst(),
        ],
        tasks=[
            fundamental_analysis_task(ticker),
        ]
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "NVDA"
    report = fundamental_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_fundamental_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")