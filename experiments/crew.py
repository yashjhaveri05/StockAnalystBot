from crewai import Crew, Process
from textwrap import dedent
from agents import StockAnalysisAgents
from tasks import StockAnalysisTasks
from dotenv import load_dotenv

load_dotenv()

class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        stock_analysis_agents = StockAnalysisAgents(self.company)
        stock_analysis_tasks = StockAnalysisTasks(self.company, stock_analysis_agents)

        agents = [
            stock_analysis_agents.fundamental_analyst(),
            stock_analysis_agents.technical_analyst(),
            stock_analysis_agents.news_sentiment_analyst(),
            stock_analysis_agents.recommendation_analyst(),
            stock_analysis_agents.future_options_analyst(),
            stock_analysis_agents.financial_analyst(),
            stock_analysis_agents.research_analyst(),
            stock_analysis_agents.investor_advisor(),
            stock_analysis_agents.report_writer()
        ]

        tasks = [
            stock_analysis_tasks.fundamental_analysis_task(),
            stock_analysis_tasks.technical_analysis_task(),
            stock_analysis_tasks.news_analysis_task(),
            stock_analysis_tasks.recommendation_analysis_task(),
            stock_analysis_tasks.future_options_analysis_task(),
            stock_analysis_tasks.financial_analysis_task(),
            stock_analysis_tasks.research_task(),
            stock_analysis_tasks.investment_advice_task(),
            stock_analysis_tasks.report_writing_task()
        ]

        stock_analysis_crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential
        )

        result = stock_analysis_crew.kickoff(inputs={'ticker': self.company})
        return result

if __name__ == "__main__":
    print("## Welcome to Financial Analysis Crew")
    print('-------------------------------')
    company = input(dedent("""
        What is the company you want to analyze? Please provide the Company Ticker
    """))

    financial_crew = FinancialCrew(company)
    result = financial_crew.run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)