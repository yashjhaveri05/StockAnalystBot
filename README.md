# PROMPT:

I want to build a stock analysis agent that provides stock reports and recommendations.
Input: Stock Ticker
Output:
1. Comprehensive report about the stock including fundamental, technical, sector analysis and stock advice
2. Fundamental Report with fundamental summary with verdict: rating out of 5
3. Technical Report with technical summary
4. Investable or not

Rough Idea:
Agents: Fundamental Agent, Technical Agent, Market Agent, Research Agent, Financial Analyst Agent, Report Writer Expert Agent, Recommender Agent
Tasks: NewsAnalysis, FundamentalAnalysis, TechnicalAnalysis, RecommendationTrendsAnalysis, HistoricalDataAnalysis, CompanyFinancialAnalysis, etc.
Tools: news data, stock historical data, stock (1month or 1 week) data, fundamental information about company, company finance reports and financial performance data, company investor data, company recommendation trends, etc.

The report generated must of this format:
Company Name
What the company does
Company Information
Company Fundamental analysis summary with metrics like PE ratio, etc
Company Technical analysis summary with metrics like SMA, EMA, etc
Company Financials summary
Company Stock Holders
Company Latest News - top 3 links
Company Recommendation Trends
Company Sector, sector performance, company performance in that sector, company competitors or peers

Give the requirements for creating such a crew agent, the agents, tasks and tools required, the data requirements for each tool, the roadmap and then the code.
I will be using:
Python
CrewAI for building the agents, tasks, tools and crew
Ollama model with an option of converting to OPENAI GPT-4o model
yfinance python library for fetching the data
any other open-source data library if yfinance not staisfying requirement
any vector database of your choice if required
Langchain, Langgraph if required


********************************

To build a stock analysis agent that provides comprehensive stock reports and recommendations, we need to define the agents, tasks, and tools required, as well as outline the data requirements for each tool. Let's break this down step-by-step.

# Requirements

### Agents:

1. Fundamental Agent: Performs fundamental analysis of the company.
2. Technical Agent: Conducts technical analysis of the stock.
3. Market Agent: Provides market and sector analysis.
4. Research Agent: Collects and analyzes news and recommendation trends.
5. Financial Analyst Agent: Analyzes company financials.
6. Report Writer Expert Agent: Compiles and formats the final report.
7. Recommender Agent: Provides investment recommendations.

### Tasks:

1. NewsAnalysis: Gathers and analyzes the latest news.
2. FundamentalAnalysis: Analyzes company fundamentals.
3. TechnicalAnalysis: Analyzes stock technical data.
4. RecommendationTrendsAnalysis: Analyzes recommendation trends.
5. HistoricalDataAnalysis: Analyzes historical stock data.
6. CompanyFinancialAnalysis: Analyzes company financial reports.
7. SectorAnalysis: Analyzes the sector performance and competitors.

### Tools:

1. yfinance: Fetches historical and real-time stock data.
2. News API: Gathers latest news about the company.
3. Financial Data API: Provides fundamental and financial data.
4. Recommendation Trends API: Collects recommendation trends data.

### Data Requirements:

1. Fundamental Data: PE ratio, earnings, dividends, etc.
2. Technical Data: SMA, EMA, volume, price patterns, etc.
3. Financial Reports: Income statement, balance sheet, cash flow.
4. Market Data: Sector performance, competitors.
5. News Data: Latest news articles.
6. Recommendation Trends: Analyst recommendations and ratings.

### Roadmap
1. Define Agents and Tasks: Define each agent with their roles, goals, and tasks.
2. Set Up Tools: Integrate APIs and libraries for data fetching.
3. Implement Data Collection and Analysis: Write code to fetch and analyze data.
4. Build and Test Agents: Create agents and test their functionality.
Compile Reports: Implement the Report Writer Expert Agent to compile the final report.
5. Deploy and Iterate: Deploy the solution and iterate based on feedback.

# Implementation Plan
### Agents:

1. fundamental_agent:
  role: Fundamental Analyst
  goal: Analyze company fundamentals.
  backstory: Expert in analyzing financial health and company fundamentals.

2. technical_agent:
  role: Technical Analyst
  goal: Analyze stock technical data.
  backstory: Skilled in technical analysis to predict stock movements.

3. market_agent:
  role: Market Analyst
  goal: Provide market and sector analysis.
  backstory: Provides insights on sector performance and market trends.

4. research_agent:
  role: Research Analyst
  goal: Collect and analyze news and recommendation trends.
  backstory: Experienced in gathering and analyzing news and recommendations.

5. financial_analyst_agent:
  role: Financial Analyst
  goal: Analyze company financial reports.
  backstory: Specializes in analyzing financial statements and performance.

6. report_writer_expert_agent:
  role: Report Writer
  goal: Compile and format the final report.
  backstory: Expert in creating comprehensive and readable reports.

7. recommender_agent:
  role: Recommender
  goal: Provide investment recommendations.
  backstory: Provides investment advice based on analysis.

### Tasks

1. news_analysis_task:
  description: Gather and analyze the latest news about the company.
  expected_output: Top 3 latest news links with summary.
  agent: research_agent

2. fundamental_analysis_task:
  description: Perform fundamental analysis of the company.
  expected_output: Fundamental analysis summary with key metrics.
  agent: fundamental_agent

3. technical_analysis_task:
  description: Perform technical analysis of the stock.
  expected_output: Technical analysis summary with key metrics.
  agent: technical_agent

4. recommendation_trends_analysis_task:
  description: Analyze recommendation trends for the stock.
  expected_output: Summary of recommendation trends and analyst ratings.
  agent: research_agent

5. historical_data_analysis_task:
  description: Analyze historical stock data.
  expected_output: Summary of historical stock performance.
  agent: technical_agent

6. company_financial_analysis_task:
  description: Analyze company financial reports.
  expected_output: Summary of financial performance.
  agent: financial_analyst_agent

7. sector_analysis_task:
  description: Analyze the sector performance and competitors.
  expected_output: Summary of sector performance and company position.
  agent: market_agent

8. report_compilation_task:
  description: Compile the final report.
  expected_output: Comprehensive report with all analysis.
  agent: report_writer_expert_agent

9. investment_recommendation_task:
  description: Provide investment recommendations based on the analysis.
  expected_output: Investment recommendation with rating.
  agent: recommender_agent

### Tools

import yfinance as yf \
import requests

#### class StockDataTool:

    def get_historical_data(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.history(period="1y")

    def get_current_data(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.info

#### class NewsTool:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_latest_news(self, ticker):
        url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={self.api_key}"
        response = requests.get(url)
        return response.json()

#### class FinancialDataTool:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_financial_data(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

#### class RecommendationTrendsTool:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_recommendation_trends(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{ticker}?apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

### Agents.py

from crewai import Agent, Task, Crew, Process \
from tools import StockDataTool, NewsTool, FinancialDataTool, RecommendationTrendsTool

##### Initialize tools
stock_data_tool = StockDataTool()
news_tool = NewsTool(api_key="your_news_api_key")
financial_data_tool = FinancialDataTool(api_key="your_financial_data_api_key")
recommendation_trends_tool = RecommendationTrendsTool(api_key="your_recommendation_trends_api_key")

##### Create agents
fundamental_agent = Agent(
    role='Fundamental Analyst',
    goal='Analyze company fundamentals.',
    tools=[financial_data_tool]
) \
technical_agent = Agent(
    role='Technical Analyst',
    goal='Analyze stock technical data.',
    tools=[stock_data_tool]
) \
market_agent = Agent(
    role='Market Analyst',
    goal='Provide market and sector analysis.',
    tools=[]
) \
research_agent = Agent(
    role='Research Analyst',
    goal='Collect and analyze news and recommendation trends.',
    tools=[news_tool, recommendation_trends_tool]
) \
financial_analyst_agent = Agent(
    role='Financial Analyst',
    goal='Analyze company financial reports.',
    tools=[financial_data_tool]
) \
report_writer_expert_agent = Agent(
    role='Report Writer',
    goal='Compile and format the final report.',
    tools=[]
) \
recommender_agent = Agent(
    role='Recommender',
    goal='Provide investment recommendations.',
    tools=[]
)

### Tasks.py

##### Define tasks
news_analysis_task = Task(
    description="Gather and analyze the latest news about the company.",
    expected_output="Top 3 latest news links with summary.",
    agent=research_agent,
    tools=[news_tool]
) \
fundamental_analysis_task = Task(
    description="Perform fundamental analysis of the company.",
    expected_output="Fundamental analysis summary with key metrics.",
    agent=fundamental_agent,
    tools=[financial_data_tool]
) \
technical_analysis_task = Task(
    description="Perform technical analysis of the stock.",
    expected_output="Technical analysis summary with key metrics.",
    agent=technical_agent,
    tools=[stock_data_tool]
) \
recommendation_trends_analysis_task = Task(
    description="Analyze recommendation trends for the stock.",
    expected_output="Summary of recommendation trends and analyst ratings.",
    agent=research_agent,
    tools=[recommendation_trends_tool]
) \
historical_data_analysis_task = Task(
    description="Analyze historical stock data.",
    expected_output="Summary of historical stock performance.",
    agent=technical_agent,
    tools=[stock_data_tool]
) \
company_financial_analysis_task = Task(
    description="Analyze company financial reports.",
    expected_output="Summary of financial performance.",
    agent=financial_analyst_agent,
    tools=[financial_data_tool]
) \
sector_analysis_task = Task(
    description="Analyze the sector performance and competitors.",
    expected_output="Summary of sector performance and company position.",
    agent=market_agent,
    tools=[]
) \
report_compilation_task = Task(
    description="Compile the final report.",
    expected_output="Comprehensive report with all analysis.",
    agent=report_writer_expert_agent,
    tools=[]
) \
investment_recommendation_task = Task(
    description="Provide investment recommendations based on the analysis.",
    expected_output="Investment recommendation with rating.",
    agent=recommender_agent,
    tools=[]
)

### Crew

##### Forming the stock analysis crew
crew = Crew(
    agents=[
        fundamental_agent, technical_agent, market_agent,
        research_agent, financial_analyst_agent, report_writer_expert_agent, recommender_agent
    ],
    tasks=[
        news_analysis_task, fundamental_analysis_task, technical_analysis_task,
        recommendation_trends_analysis_task, historical_data_analysis_task,
        company_financial_analysis_task, sector_analysis_task,
        report_compilation_task, investment_recommendation_task
    ],
    process=Process.sequential
)

##### Kickoff the crew with a sample input
result = crew.kickoff(inputs={'ticker': 'AAPL'}) \
print(result)

# Deploy and Iterate

Deploy the solution on a server or cloud environment.
Test the agents with various stock tickers.
Iterate based on feedback and improve the agents, tasks, and tools.

This is a comprehensive plan to build your stock analysis agent using CrewAI. If you have any specific questions or need further customization, feel free to ask!
