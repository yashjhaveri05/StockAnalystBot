from crewai import Task

class StockAnalysisTasks:
    def __init__(self, ticker, stock_analysis_agents):
        self.agents = stock_analysis_agents
        self.ticker = ticker

    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
    
    def fundamental_analysis_task(self):
        return Task(
            description=f"""Analyze the fundamental data of the company {self.ticker} and provide a comprehensive report.
            Include company information, historical data, dividend and stock split timeline, share count, top shareholders, financial statements, earnings and earning forecast, price target, market trends, economic factors, and sustainability.
            Your objective is to identify undervalued stocks and advise on potential investment opportunities.
            {self.__tip_section()}""",
            expected_output=f"""A detailed report on {self.ticker} including all fundamental analysis aspects. The report should provide clear investment recommendations.""",
            agent=self.agents.fundamental_analyst()
        )

    def technical_analysis_task(self):
        return Task(
            description=f"""Analyze the technical data of the specified stock {self.ticker} and identify key trends, patterns, and technical indicators.
            {self.__tip_section()}""",
            expected_output=f"""A technical analysis report on {self.ticker} highlighting key trends, patterns, and indicators.""",
            agent=self.agents.technical_analyst()
        )

    def news_analysis_task(self):
        return Task(
            description=f"""Analyze the latest news related to the specified stock {self.ticker} and assess the overall sentiment.
            {self.__tip_section()}""",
            expected_output=f"""A sentiment analysis report on {self.ticker} based on the latest news articles and media coverage.""",
            agent=self.agents.news_sentiment_analyst()
        )

    def recommendation_analysis_task(self):
        return Task(
            description=f"""Analyze analyst recommendations and provide a summary of their sentiment towards the specified stock {self.ticker}.
            {self.__tip_section()}""",
            expected_output=f"""A summary report of analyst recommendations and market outlooks for {self.ticker}.""",
            agent=self.agents.recommendation_analyst()
        )

    def future_options_analysis_task(self):
        return Task(
            description=f"""Analyze futures and options data for the specified stock {self.ticker} and provide insights on market expectations.
            {self.__tip_section()}""",
            expected_output=f"""A report on futures and options data for {self.ticker}, including market expectations and potential movements.""",
            agent=self.agents.future_options_analyst()
        )

    def financial_analysis_task(self):
        return Task(
            description=f"""Conduct a comprehensive financial analysis of {self.ticker}, including macroeconomic data, fundamental data, news sentiment, analyst recommendations, and futures and options data.
            {self.__tip_section()}""",
            expected_output=f"""A detailed financial analysis report on {self.ticker}, encompassing all aspects of macroeconomic, fundamental, news, recommendations, and futures/options data.""",
            agent=self.agents.financial_analyst(),
            dependencies=[
                self.fundamental_analysis_task(),
                self.news_analysis_task(),
                self.recommendation_analysis_task()
            ]
        )

    def research_task(self):
        return Task(
            description=f"""Gather and interpret data related to {self.ticker} and provide a comprehensive report. Include fundamental data, news sentiment, and analyst recommendations.
            {self.__tip_section()}""",
            expected_output=f"""A detailed research report on {self.ticker}, including fundamental data, news sentiment, and analyst recommendations.""",
            agent=self.agents.research_analyst()
        )

    def investment_advice_task(self):
        return Task(
            description=f"""Provide a comprehensive investment recommendation for {self.ticker}, combining macroeconomic data, fundamental data, technical analysis, news sentiment, analyst recommendations, and futures/options data.
            {self.__tip_section()}""",
            expected_output=f"""A detailed investment recommendation report for {self.ticker}, incorporating insights from all relevant data sources.""",
            agent=self.agents.investor_advisor(),
            dependencies=[
                self.technical_analysis_task(),
                self.future_options_analysis_task(),
                self.financial_analysis_task(),
                self.research_task()
            ]
        )

    def report_writing_task(self):
        return Task(
            description=f"""Compile a detailed report based on the comprehensive analysis of the specified stock {self.ticker}.
            {self.__tip_section()}""",
            expected_output=f"""A comprehensive financial report on {self.ticker}, synthesizing data from various analyses into a coherent document.""",
            agent=self.agents.report_writer(),
            dependencies=[
                self.technical_analysis_task(),
                self.future_options_analysis_task(),
                self.financial_analysis_task(),
                self.research_task(),
                self.investment_advice_task()
            ]
        )