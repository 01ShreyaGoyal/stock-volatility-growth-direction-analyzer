# Stock Volatility and Growth Direction Analyzer
#### Video URL:<https://youtu.be/PESQmRyyfB0>
#### **Description :**

This project analyzes historical stock price behavior by calculating volatility and assessing basic growth direction over a user-specified period. The program retrieves historical price data, computes returns based on the chosen frequency (weekly, monthly, or yearly), and derives volatility as a measure of price variability. It also evaluates growth direction by comparing initial and final prices, providing a straightforward indication of price movement trend.

The program accepts the following user inputs:
  1. Company Ticker Symbol: The stock ticker of the company to be analyzed.

  2. Start Date: The beginning date of the analysis period.

  3. End Date: The ending date of the analysis period.

  4. Frequency: The time interval for analysis, allowing the user to choose between weekly, monthly, or yearly calculations.

After collecting user inputs, the program retrieves historical price data using the yfinance library. From the retrieved dataset, the adjusted closing price (“Adj Close”) is selected for analysis. The data is then resampled according to the selected frequency.

Returns are calculated from the resampled prices. Simple returns are used for weekly and monthly analysis, while logarithmic returns are used for yearly analysis. Volatility is computed as the standard deviation of these returns.

The program also evaluates the overall growth direction by comparing the initial and final adjusted closing prices for the selected period. Thus providing a simple indication of whether stock exhibited upward, downward or no significant price movement.

Period volatility is annualized and then classified as low, moderate, or high using fixed heuristic thresholds. The final analysis result is displayed as a combination of volatility classification and growth direction.

#### **Assumptions and Limitations :**

Analysis is entirely historical and descriptive rather than predictive. Annualization of volatility assumes constant volatility and stationary market conditions. Growth direction is determined using only the starting and ending prices and does not measure growth rates or long-term trends. Volatility thresholds (Low: <15%, Moderate: 15-30%, High: >30%) are heuristic, not industry benchmarks. The results depend on data availability and quality from Yahoo Finance.

#### **Files and Structure :**

project.py - contains the complete implementation, including data retrieval, resampling, return calculations, volatility computation, growth direction analysis, and user interaction.

test_project.py - contains unit tests written using pytest to validate key computational functions such as resampling, return calculation, volatility computation, and growth direction logic.

requirements.txt - lists all external dependencies required to run the project.

readme.md - comprehensive docmentation of the entire project.

#### **Design Choices :**

Adjusted closing prices are used to account for stock splits and dividends, ensuring more accurate return and volatility calculations. Different return measures are selected based on analysis frequency. Simple returns are used for weekly and monthly analysis due to their intuitive interpretation over shorter horizons, while log returns are used for yearly analysis as they are more appropriate for longer time horizons.

#### **Output Interpretation :**

The output shows two volatility measures:
  1. Period Volatility: Actual volatility for user selected frequency.
  2. Annualized Volatility: Scaled to yearly basis for comparison.

Example Output :

Average Return for chosen period: 1.512%

Period Volatility: 6.273%, Annualized Volatility: 21.729%

Final Analysis Result (based on annualized volatility):

Moderate Volatility with upward price trend.

Interpretation :

  1. Monthly returns varied by 6.27% on average

  2. Annualized equivalent is 21.73% (6.273% × √12)

  3. 21.73% = "Moderate Volatility" (15-30% range)

  4. "Upward trend" = Stock price ended higher than it started.
