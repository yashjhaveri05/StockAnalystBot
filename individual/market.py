# import os
# from dotenv import load_dotenv
# load_dotenv()
# import yfinance as yf
# from crewai_tools import tool
# from crewai import Agent, Task, Crew
# from langchain_google_genai import ChatGoogleGenerativeAI
# from datetime import datetime

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

# # Define tools
# def get_last_10_years_inflation(api_key: str):
#     url = f"https://www.alphavantage.co/query?function=INFLATION&apikey={api_key}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return "Failed to retrieve data"
#     data = response.json()
#     if "data" not in data:
#         return "No data found"
#     count = 0
#     last_10_years_data = {}
#     for entry in data['data']:
#         if count <= 10:
#             last_10_years_data[entry['date']] = f"{entry['value']}{data['unit']}"
#             count += 1
#         else:
#             break
#     return last_10_years_data

# def get_cpi(api_key: str):
#     url = f"https://www.alphavantage.co/query?function=CPI&apikey={api_key}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return "Failed to retrieve data"
#     data = response.json()
#     if "data" not in data:
#         return "No data found"
#     count = 0
#     required_data = {}
#     for entry in data['data']:
#         if count <= 25:
#             required_data[entry['date']] = f"{entry['value']}{data['unit']}"
#             count += 1
#         else:
#             break
#     return required_data

# def get_interest_rate(api_key: str):
#     url = f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={api_key}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return "Failed to retrieve data"
#     data = response.json()
#     if "data" not in data:
#         return "No data found"
#     count = 0
#     required_data = {}
#     for entry in data['data']:
#         if count <= 48:
#             required_data[entry['date']] = f"{entry['value']}{data['unit']}"
#             count += 1
#         else:
#             break
#     return required_data

# def get_last_10_years_gdp(api_key: str):
#     url = f"https://www.alphavantage.co/query?function=REAL_GDP&apikey={api_key}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return "Failed to retrieve data"
#     data = response.json()
#     if "data" not in data:
#         return "No data found"
#     count = 0
#     last_10_years_data = {}
#     for entry in data['data']:
#         if count <= 10:
#             last_10_years_data[entry['date']] = f"{entry['value']}{data['unit']}"
#             count += 1
#         else:
#             break
#     return last_10_years_data

# @tool("Get macro Economic Data")
# def get_macro_economic(ticker):
#     """Useful to retrieve macro economic indicators and returns 
#         gdp data, inflation data and interest rate data."""
#     api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

#     macro_data = {
#         "gdp": get_last_10_years_gdp(api_key),
#         "cpi": get_cpi(api_key),
#         "inflation": get_last_10_years_inflation(api_key),
#         "interest_rate": get_interest_rate(api_key)
#     }
#     return str(macro_data)

# # Define agents
# def macro_data_agent():
#     return Agent(
#         role='Advanced Economic Analyst',
#         goal="Retrieve and summarize macroeconomic indicators for analysis.",
#         backstory="You are an economic analyst responsible for monitoring and analyzing macroeconomic indicators such as GDP, inflation, and interest rates.",
#         verbose=True,
#         tools=[
#             get_macro_economic
#         ],
#         llm = llm
#     )

# # Define tasks
# def macro_data_task (ticker):
#     return Task(
#         description=f"Retrieve and summarize macroeconomic indicators for {ticker} ticker symbol.",
#         expected_output=f"A summary report of the overall market including GDP data, cpi, inflation data, and interest rate data.",
#         agent=macro_data_agent(),
#         async_execution=True,
#     )

# # Form the crew and kickoff with user-provided stock input
# def market_crew(ticker):
#     crew = Crew(
#         agents=[
#             macro_data_agent()
#         ],
#         tasks=[
#             macro_data_task(ticker)
#         ]
#     )
    
#     result = crew.kickoff(inputs={'ticker': ticker})
#     return result

# if __name__ == "__main__":
#     stock_ticker = "AAPL"
#     report = market_crew(stock_ticker)
#     today_date = datetime.now().strftime("%Y-%m-%d")
#     file_name = f"{stock_ticker}_fundamental_{today_date}.txt"
#     folder_path = f"../reports/{today_date}/{stock_ticker}"
#     os.makedirs(folder_path, exist_ok=True)
#     file_path = os.path.join(folder_path, file_name)
#     with open(file_path, "w") as file:
#         file.write(report)
#     print(f"Report saved to {file_path}")