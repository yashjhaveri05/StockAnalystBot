from crewai import Agent
from tools import (
    MacroEconomicDataTool,
    FundamentalDataTool,
    TechnicalDataTool,
    NewsDataTool,
    RecommendationDataTool,
    FutureOptionsDataTool
)
from dotenv import load_dotenv
load_dotenv()
# from langchain_google_genai import ChatGoogleGenerativeAI
import os

# gemini_api_key = os.getenv("GEMINI_API_KEY")

class StockAnalysisAgents:
    def __init__(self, ticker):
        # self.gemini = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.5, google_api_key=gemini_api_key)
        self.ticker = ticker
        self.fundamental = FundamentalDataTool(self.ticker)
        self.technical = TechnicalDataTool(self.ticker)
        self.news = NewsDataTool(self.ticker)
        self.recommendation = RecommendationDataTool(self.ticker)
        self.futureoptions = FutureOptionsDataTool(self.ticker)
        self.macro = MacroEconomicDataTool(self.ticker)

    def fundamental_analyst(self):
        return Agent(
            role='Elite Fundamental Analyst',
            goal="""Perform a meticulous analysis of the company's financial health, including historical data, dividend records, stock splits, share counts, major shareholders, financial statements, earnings reports, and forecasts. Provide investment recommendations by identifying undervalued stocks and predicting potential growth opportunities.""",
            backstory="""A highly experienced financial analyst renowned for in-depth fundamental analysis and strategic investment advice, committed to delivering exceptional insights for a high-profile client.""",
            verbose=True,
            tools=[
                self.fundamental.get_fundamentals,
                self.fundamental.get_data,
                self.fundamental.get_shareholders,
                self.fundamental.get_financials,
                self.macro.get_macro_economic
            ],
            # llm=self.gemini,
        )

    def technical_analyst(self):
        return Agent(
            role='Master Technical Analyst and Chartist',
            goal="""Examine and interpret the technical aspects of the stock, including chart patterns, trading volumes, and technical indicators. Identify trends and forecast future stock movements to provide actionable trading insights.""",
            backstory="""A technical analysis expert with a sharp eye for detail, specializing in chart patterns and technical indicators to predict market movements with precision.""",
            verbose=True,
            tools=[
                self.technical.get_data
            ],
            # llm=self.gemini,
        )

    def news_sentiment_analyst(self):
        return Agent(
            role='Top News and Sentiment Analyst',
            goal="""Evaluate the latest news and media coverage related to the stock. Assess overall market sentiment and its potential impact on stock performance, providing insights into market dynamics and investor behavior.""",
            backstory="""A market sentiment specialist with a deep understanding of news analysis, skilled in gauging the impact of media coverage on stock performance and investor attitudes.""",
            verbose=True,
            tools=[
                self.news.get_news
            ],
            # llm=self.gemini,
        )

    def recommendation_analyst(self):
        return Agent(
            role='Premier Recommendation Analyst',
            goal="""Analyze and summarize analyst recommendations and market outlooks for the specified stock. Provide a comprehensive summary of sentiments from various market experts.""",
            backstory="""An expert in synthesizing analyst opinions, known for delivering clear and concise summaries of market sentiments and recommendations from top financial experts.""",
            verbose=True,
            tools=[
                self.recommendation.get_recommendations
            ],
            # llm=self.gemini,
        )

    def future_options_analyst(self):
        return Agent(
            role='Advanced Futures and Options Analyst',
            goal="""Investigate futures and options data to offer insights into market expectations and potential movements. Analyze earnings forecasts and market trends to predict future stock performance.""",
            backstory="""A seasoned analyst with extensive experience in futures and options markets, adept at interpreting complex data to forecast potential market shifts and opportunities.""",
            verbose=True,
            tools=[
                self.futureoptions.get_futures,
                self.futureoptions.get_options
            ],
            # llm=self.gemini,
        )

    def financial_analyst(self):
        return Agent(
            role='Chief Financial Analyst',
            goal="""Deliver comprehensive financial insights and market trend analysis to impress high-profile clients. Combine macroeconomic data, fundamental and technical analysis, news sentiment, and recommendations to provide holistic investment advice.""",
            backstory="""A distinguished financial analyst with a broad skill set encompassing various aspects of market analysis, dedicated to providing unparalleled investment recommendations for prestigious clients.""",
            verbose=True,
            tools=[
                # self.macro.get_macro_economic, 
                # self.fundamental.get_fundamentals,
                # self.fundamental.get_data,
                # self.fundamental.get_shareholders,
                # self.fundamental.get_financials, 
                # self.news.get_news, 
                # self.recommendation.get_recommendations, 
            ],
            allow_delegation=True,
            # llm=self.gemini,
        )

    def research_analyst(self):
        return Agent(
            role='Leading Research Analyst',
            goal="""Gather, interpret, and present data effectively to astound clients with comprehensive research reports. Analyze fundamental data, news sentiment, and recommendations to deliver insightful findings.""",
            backstory="""Recognized as the top research analyst, renowned for exceptional skills in data interpretation and report generation, currently engaged with an important client to deliver outstanding research insights.""",
            verbose=True,
            # llm=self.gemini,
            tools=[
                # self.fundamental.get_fundamentals,
                # self.fundamental.get_data,
                # self.fundamental.get_shareholders,
                # self.fundamental.get_financials,
                # self.news.get_news, 
                # self.recommendation.get_recommendations
            ]
        )

    def investor_advisor(self):
        return Agent(
            role='Senior Investment Advisor',
            goal="""Provide full-spectrum stock analysis and investment recommendations to impress high-profile clients. Integrate macroeconomic trends, fundamental and technical analysis, news sentiment, recommendations, and options data to formulate strategic advice.""",
            backstory="""An experienced investment advisor with a proven track record of combining diverse analytical insights to craft strategic investment plans, dedicated to impressing top-tier clients.""",
            verbose=True,
            tools=[
                # self.macro.get_macro_economic, 
                # self.fundamental.get_fundamentals,
                # self.fundamental.get_data,
                # self.fundamental.get_shareholders,
                # self.fundamental.get_financials,
                # self.technical.get_data,
                # self.news.get_news, 
                # self.recommendation.get_recommendations, 
                # self.futureoptions.get_futures,
                # self.futureoptions.get_options
            ],
            allow_delegation=True,
            # llm=self.gemini,
        )

    def report_writer(self):
        return Agent(
            role='Expert Financial Report Writer',
            goal="""Compile detailed and coherent reports based on all the comprehensive stock analysis. Synthesize data from various analyses into a well-structured document for stakeholders.""",
            backstory="""An accomplished report writer with extensive experience in transforming complex data into clear, informative reports, adept at delivering high-quality documentation for stakeholders.""",
            verbose=True,
            tools=[
                # self.macro.get_macro_economic, 
                # self.fundamental.get_fundamentals,
                # self.fundamental.get_data,
                # self.fundamental.get_shareholders,
                # self.fundamental.get_financials,
                # self.technical.get_data,
                # self.news.get_news, 
                # self.recommendation.get_recommendations, 
                # self.futureoptions.get_futures,
                # self.futureoptions.get_options
            ],
            # llm=self.gemini,
        )
