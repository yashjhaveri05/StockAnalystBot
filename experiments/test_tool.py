import yfinance as yf
import requests
from langchain.tools import tool

class NewsDataTool:
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)

    @tool("Get Company News")
    def get_news(self):
        """Useful to retrieve news about a company, stock or any other
        topic and return relevant results"""""
        news = self.stock.news
        string = []

        for n in news:
            try:
                string.append('\n'.join([
                    f"Title: {n['title']}", f"Link: {n['link']}",
                    f"Publisher: {n['publisher']}", "\n-----------------"
                ]))
            except KeyError:
                next
        return '\n'.join(string)