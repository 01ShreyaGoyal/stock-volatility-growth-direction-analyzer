import pandas as pd
from project import (resampling,calc_returns,calc_volatility,growth_direction)

def sample_price_df():
    dates = pd.date_range("2025-01-01",periods=6,freq="D")
    prices = [100,102,101,103,104,104]
    df = {"Adj Close":prices}
    price_df = pd.DataFrame(df,index=dates)
    return price_df

def test_resampling():
    df= sample_price_df()
    assert resampling(df,"5") == "Frequency must be either 1, 2 or 3"
    assert resampling(df,"3") == "Yearly Volatility calculation requires atleast 2 years of data."

def test_calc_returns():
    df = sample_price_df()
    returns = calc_returns(df,"1")
    assert len(returns) == len(df)-1

def test_calc_volatility():
    df = sample_price_df()
    df.rename(columns={"Adj Close":"Return_Val"},inplace=True)
    sd= df["Return_Val"].var() ** 0.5
    assert calc_volatility(df)==sd

def test_growth_direction():
    df = sample_price_df()
    assert growth_direction(df)=="Upward"
