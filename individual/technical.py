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

"""
technical metrics: 
Simple Moving Average (SMA), Exponential Moving Average (EMA), Weighted Moving Average (WMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), ATR and Bollinger Bands, Stochastic Oscillator, Average Directional Index (ADX), On-Balance Volume (OBV), Fibonacci Retracement, Price Rate of Change (ROC), Parabolic SAR (Stop and Reverse), Average True Range (ATR), Commodity Channel Index (CCI), Chaikin Money Flow (CMF), Ichimoku Cloud, Volume Weighted Average Price (VWAP), Renko, Volatility Measure, Sharpe and Sortino Ratio, Calmar Ratio, Maximum Drawdown, Piotroski F-Score
"""
# Define tools
@tool("Get 1 year historical data")
def get_1_year_historical_data(ticker: str) -> str:
    """Useful to retrieve the daily historical data for the last 1 years about a company or stock
        and return the date, OHLC, volume, dividends and stock splits for that date"""
    stock = yf.Ticker(ticker)
    data = stock.history(period='1y')
    if data.empty:
        return "No historical data available."
    return data.to_string()

# Define agents
def technical_analyst():
    return Agent(
        role='Master Technical Analyst and Chartist',
        goal="Examine and interpret the technical aspects of the stock, including chart patterns, trading volumes, and technical indicators. Identify trends and forecast future stock movements to provide actionable trading insights. Also, calculate and provide Simple Moving Average (SMA), Exponential Moving Average (EMA), Weighted Moving Average (WMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD)",
        backstory="A technical analysis expert with a sharp eye for detail, specializing in chart patterns and technical indicators to predict market movements with precision.",
        verbose=True,
        tools=[
            get_1_year_historical_data
        ],
        llm = llm
    )

# Define tasks
def technical_analysis_task(ticker):
    return Task(
        description=f"Examine and interpret the technical aspects of the stock, including chart patterns, trading volumes, and technical indicators. Identify trends and forecast future stock movements to provide actionable trading insights.Also, calculate and provide Simple Moving Average (SMA), Exponential Moving Average (EMA), Weighted Moving Average (WMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD).",
        expected_output=f"A technical analysis report on {ticker} highlighting key trends with reason, forecast with reason, patterns, and technical indicators. Aslo, provide a brief about each of the technical terms used.",
        agent=technical_analyst(),
    )

# Form the crew and kickoff with user-provided stock input
def technical_crew(ticker):
    crew = Crew(
        agents=[
            technical_analyst()
        ],
        tasks=[
            technical_analysis_task(ticker)
        ]
    )
    result = crew.kickoff(inputs={'ticker': ticker})
    return result

if __name__ == "__main__":
    stock_ticker = "NVDA"
    report = technical_crew(stock_ticker)
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{stock_ticker}_technical_{today_date}.txt"
    folder_path = f"../reports/{today_date}/{stock_ticker}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        file.write(report)
    print(f"Report saved to {file_path}")