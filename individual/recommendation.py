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

# Define agents
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

# Define tasks
def recommendation_analysis_task(ticker):
    return Task(
        description=f"Analyze analyst recommendations and provide a summary of their sentiment towards the specified stock {ticker}.",
        expected_output=f"A summary report of analyst recommendations and market outlooks for {ticker}. Provide a summary of the recommendation sentiments and other trends showing positive/negative/neutrality for the stock.",
        agent=recommendation_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def recommendation_crew(ticker):
    crew = Crew(
        agents=[
            recommendation_analyst()
        ],
        tasks=[
            recommendation_analysis_task(ticker)
        ],
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "AAPL"
    report = recommendation_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_recommendation_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")