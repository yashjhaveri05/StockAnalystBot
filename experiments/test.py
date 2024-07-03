import yfinance as yf
import requests

stock = yf.Ticker("NVDA")

# fundamental_analyst         -> fundamental_analysis_task
# technical_analyst           -> technical_analysis_task
# news_sentiment_analyst      -> news_analysis_task
# recommendation_analyst      -> recommendation_analysis_task
# future_options_analyst      -> future_options_analysis_task
# financial_analyst           -> financial_analysis_task
# research_analyst            -> research_task
# investor_advisor            -> investment_advice_task
# report_writer               -> report_writing_task