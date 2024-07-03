from crewai import Agent
from test_tool import NewsDataTool
from dotenv import load_dotenv
import os
load_dotenv()

class StockAnalysisAgents:
    def __init__(self, ticker):
        self.ticker = ticker
        self.news = NewsDataTool(ticker)
    
    def news_sentiment_analyst(self):
        return Agent(
            role='Top News and Sentiment Analyst',
            goal="""Evaluate the latest news and media coverage related to the stock. Assess overall market sentiment and its potential impact on stock performance, providing insights into market dynamics and investor behavior.""",
            backstory="""A market sentiment specialist with a deep understanding of news analysis, skilled in gauging the impact of media coverage on stock performance and investor attitudes.""",
            verbose=True,
            tools=[
                self.news.get_news
            ]
        )

# Example usage
agent = StockAnalysisAgents("NVDA").news_sentiment_analyst()
print(agent)
