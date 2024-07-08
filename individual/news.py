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

# Define tasks
def news_analysis_task(ticker):
    return Task(
        description=f"Evaluate the latest news and media coverage related to the stock. Assess overall market sentiment and its potential impact on stock performance, providing insights into market dynamics and investor behavior.",
        expected_output=f"A sentiment analysis report on {ticker} based on the latest news articles and media coverage, with potential imapct and upward/downward movement of data. Also, include the top 5 news.",
        agent=news_sentiment_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def news_crew(ticker):
    crew = Crew(
        agents=[
            news_sentiment_analyst()
        ],
        tasks=[
            news_analysis_task(ticker)
        ],
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "NVDA"
    report = news_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_news_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")