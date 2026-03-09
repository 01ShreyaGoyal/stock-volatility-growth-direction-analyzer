import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def get_data(ticker,start_date,end_date):
    try:
      s_d= datetime.strptime(start_date,'%Y-%m-%d')
      e_d= datetime.strptime(end_date,'%Y-%m-%d')
      today=datetime.now()
      if s_d>=e_d:
          return(f'End Date must be greater than Start Date')
      if e_d>today:
        return(f"Input Date can't be in future. Today is {today.date()}")
    except ValueError:
      return "Date entered is either invalid or not in correct format."

    try:
        data= yf.download(ticker,start_date, end_date,auto_adjust=False,progress=False)

    except Exception as e:
        return f'Data fetch failed: {e}'

    if not data.empty:
        df=data[['Adj Close']].dropna()
        if len(df)<2:
          return "Insufficient Data"
        return (df)
    else:
        return f"Invalid ticker or no data available"

def resampling(price_df,freq):

  if not isinstance(price_df,pd.DataFrame):
    return price_df

  if freq not in ["1","2","3"]:
    return "Frequency must be either 1, 2 or 3"
  freq_dict={1:"W-FRI",2:"ME",3:"YE"}
  resampled_data= price_df.resample(freq_dict[int(freq)]).last().dropna()

  if len(resampled_data)<2:
    if freq=="1":
      return "Weekly Volatility calculation requires atleast 2 weeks of data."
    elif freq=="2":
      return "Monthly Volatility calculation requires atleast 2 months of data."
    elif freq=="3":
      return "Yearly Volatility calculation requires atleast 2 years of data."

  return resampled_data

def calc_returns(resampled_prices,freq):

  if not isinstance(resampled_prices,pd.DataFrame):
    return resampled_prices

  if freq in ["1","2"]:
    returns = (resampled_prices/resampled_prices.shift(1))-1

  elif freq=="3":
    returns= np.log(resampled_prices/resampled_prices.shift(1))

  returns=returns.dropna()
  returns.rename(columns={'Adj Close':'Return_Val'},inplace=True)
  return returns

def calc_volatility(returns):
  if not isinstance(returns,pd.DataFrame):
    return returns

  if len(returns)<2:
    return"Data Insufficient as atleast two returns are required to calculate volatility"

  variance= returns['Return_Val'].var()
  volatility= variance**0.5

  return volatility.iloc[0] if isinstance(volatility,pd.Series) else volatility


def growth_direction(price_df):
  if not isinstance(price_df,pd.DataFrame):
    return price_df

  if len(price_df)<2:
    return "At least two values required for determining growth direction"

  start_price= price_df["Adj Close"].iloc[0].item()
  end_price = price_df["Adj Close"].iloc[-1].item()


  if end_price>start_price:
    return "Upward"
  elif end_price<start_price:
    return "Downward"
  else:
    return "No Change"

def interpretation(growth,volatility,freq):
  if not isinstance(volatility,(float,int)):
    return volatility


  if freq=="1":
    annual_vol=volatility* np.sqrt(52)
  elif freq=="2":
    annual_vol=volatility*np.sqrt(12)
  elif freq=="3":
    annual_vol=volatility
  else:
    return freq

  if annual_vol<0.15:
    vol_level="Low Volatility"
  elif annual_vol<0.30:
    vol_level="Moderate Volatility"
  else:
    vol_level="High Volatility"

  if growth=="Upward":
    return f"{vol_level} with upward price trend."
  elif growth=="Downward":
    return f"{vol_level} with downward price trend."
  elif growth=="No Change":
    return f"{vol_level} with no significant price change."
  else:
    return f"{vol_level} but for growth there is insufficient info."

def main():
  ticker=input("Company Ticker Name: ").upper().strip()
  start_date=input("Start Date(yyyy-mm-dd): ").strip()
  end_date= input("End Date(yyyy-mm-dd): ").strip()
  print("Select Frequency")
  print("1. Weekly" )
  print("2. Monthly")
  print("3. Yearly" )
  freq=input("Enter choice 1-3: ").strip()
  price_df=get_data(ticker,start_date,end_date)
  resampled_prices= resampling(price_df,freq)
  returns=calc_returns(resampled_prices,freq)
  volatility=calc_volatility(returns)
  growth=growth_direction(price_df)

  print(" "*50)

  print(f"{'*'*30}ANALYSIS RESULTS{'*'*35}")

  if isinstance(price_df,pd.DataFrame):
    print("Data Fetched Successfully for:")
    stock=yf.Ticker(ticker)
    info=stock.info
    print(f"  Company: {info['longName']}")
    print(f"  Sector: {info['sector']}")
    print(f"  Industry: {info['industry']}")

  if isinstance(resampled_prices,pd.DataFrame):
    print(f"-"*50)
    print(f"Resampled Data points for chosen frequency: {len(resampled_prices)}")

  if isinstance(returns,pd.DataFrame):
    print(f"Number of return points calculated: {len(returns)}")
    if len(returns)>2:
      avg_return=(returns["Return_Val"].values.mean())*100
      print(f"Average Return for chosen period: {round(avg_return,3)}%")
  if not isinstance(volatility,str):
    if freq=="1":
      annual_vol=(volatility* np.sqrt(52))*100
    elif freq=="2":
      annual_vol=(volatility*np.sqrt(12))*100
    elif freq=="3":
      annual_vol=volatility*100
    period_vol=volatility*100
    print(f"Period Volatility: {round(period_vol,3)}%, Annualized Volatility: {round(annual_vol,3)}%")
  print("-"*50)
  print("Final Analysis Result (based on annualized volatility):")
  print(interpretation(growth,volatility,freq))
  print(" - "*50)

if __name__=="__main__":
  main()
