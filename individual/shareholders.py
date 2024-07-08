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
@tool("Get shareholders information")
def get_shareholders(ticker: str) -> str:
    """Useful to retrieve shareholders in the company and categorize them. Returns the 
        major holders, institutional holders, and mutual fund holders and also returns information 
        about insider transactions, insider purchases, and insider roster holders."""
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

# Define agents
def stockholder_analyst():
    return Agent(
        role='Elite Stockholder Analyst',
        goal="Analyze the stockholder list including the major stakeholders and insider data and provide a descriptive stock analysis based on this data.",
        backstory="A highly experienced stockholder analyst renowned for in-depth analysis of insider transactions and purchases as well as the major stockholders.",
        verbose=True,
        tools=[
            get_shareholders
        ],
        llm=llm
    )

# Define tasks
def stockholder_analysis_task(ticker):
    return Task(
        description=f"Analyze the stockholder list including the major stakeholders and insider data and provide a descriptive stock analysis based on this data.",
        expected_output=f"A detailed report on {ticker} including all major and institutional stockholders. The report should provide clear sentiments based on insider data and stockholder information as well as provide investment recommendations.",
        agent=stockholder_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def shareholders_crew(ticker):
    crew = Crew(
        agents=[
            stockholder_analyst()
        ],
        tasks=[
            stockholder_analysis_task(ticker)
        ]
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "NVDA"
    report = shareholders_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_shareholders_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")
