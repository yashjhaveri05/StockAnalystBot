#### Last Update: 1 August, 2024

# StockAnalystBot

StockAnalystBot is a comprehensive stock analysis tool designed to generate detailed reports on stocks by leveraging the power of several dedicated agents. Each agent specializes in a specific area of stock analysis, ensuring that users receive a nuanced and multi-dimensional view of potential investments. The tool employs `yfinance` to fetch necessary data and utilizes the capabilities of CrewAI and Google LLM to process and analyze this data efficiently.

## Features

- **Multiple Analysis Agents**: The bot includes several specialized agents that focus on different aspects of stock analysis:
  - **Fundamental Analyst**: Evaluates the intrinsic value of a stock based on fundamental business indicators.
  - **Financial Analyst**: Analyzes the financial health and performance of a company.
  - **Technical Analyst**: Studies statistical trends gathered from trading activity.
  - **News Sentiment Analyst**: Assesses the sentiment of news articles related to the stock.
  - **Recommendation Sentiment Analyst**: Analyzes market expert recommendations.
  - **Stockholder Analyst**: Reviews the patterns and behaviors of institutional and individual stockholders.
  - **Futures Analyst**: Evaluates futures contracts to predict future performance.
  - **Options Analyst**: Analyzes options market data to gauge market sentiment and potential moves.

- **Data Efficiency**: To reduce redundant processing, StockAnalystBot caches reports based on dates, allowing it to serve previously generated reports quickly without reprocessing.

## Installation
Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yashjhaveri05/StockAnalystBot.git
```
```bash
cd StockAnalystBot
```

Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## Running the Bot
To start the bot and follow the prompts, execute the following command:

```bash
python main.py
```

## Limitations
1. **Data Freshness**: The bot relies on data that may not always be up-to-date, which could lead to inaccuracies in the analysis.
2. **Investment Decisions**: This tool should not be used as the sole source for making investment decisions, as it only predicts sentiments and trends based on available data and not on comprehensive market analysis.

## Disclaimer
- **Educational/Experimental use Only**: The tool is not built by financial experts and is intended for educational and research purposes only. Do not rely on it for investment advice.

## Contribution
Contributions to StockAnalystBot are welcome! Whether it's improving the logic, adding new features, or providing feedback, your input is valued. Please feel free to fork the repository, make changes, and submit a pull request. You can also reach out to me on: [LinkedIn](https://www.linkedin.com/in/yashj05/)

## Discussion
If you have ideas or want to discuss potential improvements, please open an issue in the GitHub repository to start a conversation or connect with me on: [LinkedIn](https://www.linkedin.com/in/yashj05/)
