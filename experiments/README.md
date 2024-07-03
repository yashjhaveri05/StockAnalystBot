1. Define Agents and Assign Tool
from crewai import Agent
from crewai_tools import tool

# Define Agents
fundamental_analyst = Agent(
    role='Fundamental Analyst',
    goal='Analyze the fundamentals of companies.',
    tools=[fundamental_tools.get_fundamentals, fundamental_tools.get_data, fundamental_tools.get_shareholders, fundamental_tools.get_financials]
)

technical_analyst = Agent(
    role='Technical Analyst',
    goal='Perform technical analysis of stock data.',
    tools=[technical_tools.get_data]
)

news_sentiment_analyst = Agent(
    role='News Sentiment Analyst',
    goal='Analyze news sentiment for companies.',
    tools=[news_tools.get_news]
)

recommendation_analyst = Agent(
    role='Recommendation Analyst',
    goal='Analyze recommendation trends for companies.',
    tools=[recommendation_tools.get_recommendations]
)

future_options_analyst = Agent(
    role='Future and Options Analyst',
    goal='Analyze futures and options data for companies.',
    tools=[future_options_tools.get_futures, future_options_tools.get_options]
)

financial_analyst = Agent(
    role='Financial Analyst',
    goal='Perform a comprehensive financial analysis.',
    tools=[],
    allow_delegation=True
)

research_analyst = Agent(
    role='Research Analyst',
    goal='Conduct thorough research on assigned topics.',
    tools=[]
)

investor_advisor = Agent(
    role='Investor Advisor',
    goal='Provide investment advice based on comprehensive analysis.',
    tools=[],
    allow_delegation=True
)

report_writer = Agent(
    role='Report Writer',
    goal='Write detailed reports based on all analyses.',
    tools=[]
)

Define Tasks and Assign Tools and Agents
from crewai import Task

# Define Tasks
fundamental_analysis_task = Task(
    description='Perform fundamental analysis on assigned companies.',
    expected_output='Detailed fundamental analysis report.',
    tools=[fundamental_tools.get_fundamentals, fundamental_tools.get_data, fundamental_tools.get_shareholders, fundamental_tools.get_financials],
    agent=fundamental_analyst
)

technical_analysis_task = Task(
    description='Perform technical analysis on stock data.',
    expected_output='Detailed technical analysis report.',
    tools=[technical_tools.get_data],
    agent=technical_analyst
)

news_analysis_task = Task(
    description='Analyze news sentiment for companies.',
    expected_output='Detailed news sentiment report.',
    tools=[news_tools.get_news],
    agent=news_sentiment_analyst
)

recommendation_analysis_task = Task(
    description='Analyze recommendation trends for companies.',
    expected_output='Detailed recommendation trends report.',
    tools=[recommendation_tools.get_recommendations],
    agent=recommendation_analyst
)

future_options_analysis_task = Task(
    description='Analyze futures and options data for companies.',
    expected_output='Detailed futures and options report.',
    tools=[future_options_tools.get_futures, future_options_tools.get_options],
    agent=future_options_analyst
)

financial_analysis_task = Task(
    description='Perform a comprehensive financial analysis.',
    expected_output='Comprehensive financial analysis report.',
    tools=[],
    agent=financial_analyst,
    dependencies=[fundamental_analysis_task, news_analysis_task, recommendation_analysis_task]
)

research_task = Task(
    description='Conduct thorough research on assigned topics.',
    expected_output='Thorough research report.',
    tools=[],
    agent=research_analyst
)

investment_advice_task = Task(
    description='Provide investment advice based on comprehensive analysis.',
    expected_output='Investment advice report.',
    tools=[],
    agent=investor_advisor,
    dependencies=[technical_analysis_task, future_options_analysis_task, financial_analysis_task, research_task]
)

report_writing_task = Task(
    description='Write detailed reports based on all analyses.',
    expected_output='Final comprehensive report.',
    tools=[],
    agent=report_writer,
    dependencies=[technical_analysis_task, future_options_analysis_task, financial_analysis_task, research_task, investment_advice_task]
)

3. Set Up the Crew and Process Configuration
from crewai import Crew, Process

# Define the Crew and Process
crew = Crew(
    agents=[
        fundamental_analyst,
        technical_analyst,
        news_sentiment_analyst,
        recommendation_analyst,
        future_options_analyst,
        financial_analyst,
        research_analyst,
        investor_advisor,
        report_writer
    ],
    tasks=[
        fundamental_analysis_task,
        technical_analysis_task,
        news_analysis_task,
        recommendation_analysis_task,
        future_options_analysis_task,
        financial_analysis_task,
        research_task,
        investment_advice_task,
        report_writing_task
    ],
    process=Process.sequential
)

# Kickoff the process
result = crew.kickoff()
print(result)