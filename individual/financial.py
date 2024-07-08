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
@tool("Get company financial data")
def get_financials(ticker: str) -> str:
    """Useful to retrieve financials of a company or stock and returns the 
        financials, income statement, balance sheet and cashflow"""
    stock = yf.Ticker(ticker)
    financials = {
        'financials': stock.financials,
        'income_stmt': stock.income_stmt,
        'balance_sheet': stock.balance_sheet,
        'cashflow': stock.cashflow
    }
    return "\n-----------------\n".join([f"{key}\n{str(val)}" for key, val in financials.items() if val is not None])

# Define agents

def financial_analyst():
    return Agent(
        role='Chief Financial Analyst',
        goal="Deliver comprehensive financial insights and market trend analysis to impress high-profile clients. Combine financial statements to provide holistic investment advice.",
        backstory="A distinguished financial analyst with a broad skill set encompassing various aspects of market analysis, dedicated to providing unparalleled insights into company financials for prestigious clients.",
        verbose=True,
        tools=[
            get_financials,
        ],
        llm = llm
    )

# Define tasks
def financial_analysis_task(ticker):
    return Task(
        description=f"Conduct a comprehensive financial analysis of {ticker}, based on the financials like income statement, balance sheet, and cashflow data.",
        expected_output=f"A detailed financial analysis report on {ticker}, encompassing all aspects of financials data like income statement, balance sheet, and cashflow data.",
        agent=financial_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def financial_crew(ticker):
    crew = Crew(
        agents=[
            financial_analyst()
        ],
        tasks=[
            financial_analysis_task(ticker)
        ]
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "NVDA"
    report = financial_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_financial_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")