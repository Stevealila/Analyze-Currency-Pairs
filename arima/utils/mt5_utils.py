def mt5_login():

    import MetaTrader5 as mt5
    from dotenv import load_dotenv 
    import os

    load_dotenv()

    EXNESS_PASSWORD = os.getenv("EXNESS_PASSWORD")
    EXNESS_SERVER = os.getenv("EXNESS_SERVER")
    EXNESS_MT5_LOGIN = os.getenv("EXNESS_MT5_LOGIN")
    try:
        mt5.login(login=int(EXNESS_MT5_LOGIN), password=EXNESS_PASSWORD, server=EXNESS_SERVER)
        print("Connected to MetaTrader5 successfully!")
    except:
        print("Failed to connect to MetaTrader5.")




def create_dataframe(currency_pair, timeframe, years_back=3):

    import MetaTrader5 as mt5
    import pytz
    from datetime import datetime
    import pandas as pd

    timeframe_map = {
        "D1": mt5.TIMEFRAME_D1,
        "H1": mt5.TIMEFRAME_H1,
        "H3": mt5.TIMEFRAME_H3,
        "H6": mt5.TIMEFRAME_H6,
        "H12": mt5.TIMEFRAME_H12,
        "M30": mt5.TIMEFRAME_M30,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1,
    }

    if timeframe.upper() not in timeframe_map:
        return "Use a different timefame"
    
    # Calculate the number of bars based on timeframe and years_back
    mt5_timeframe = timeframe_map[timeframe.upper()]
    if mt5_timeframe == mt5.TIMEFRAME_D1:  # Daily
        bars = years_back * 365 
    elif mt5_timeframe == mt5.TIMEFRAME_H1:  # Hourly
        bars = years_back * 365 * 24
    elif mt5_timeframe == mt5.TIMEFRAME_H3:  # Every 3 hours
        bars = years_back * 365 * 24 // 3
    elif mt5_timeframe == mt5.TIMEFRAME_H6:  # Every 6 hours
        bars = years_back * 365 * 24 // 6
    elif mt5_timeframe == mt5.TIMEFRAME_H12:  # Every 12 hours
        bars = years_back * 365 * 24 // 12
    elif mt5_timeframe == mt5.TIMEFRAME_M30:  # Every 30 minutes
        bars = years_back * 365 * 24 * 60 // 30
    elif mt5_timeframe == mt5.TIMEFRAME_W1:  # Weekly
        bars = years_back * 52  
    elif mt5_timeframe == mt5.TIMEFRAME_MN1:  # Monthly
        bars = years_back * 12  
    else:
        bars = years_back * 365  # Default to daily bars

    rates = mt5.copy_rates_from(
        currency_pair.upper()+"m", 
        mt5_timeframe, 
        datetime.now(pytz.timezone("Africa/Nairobi")), 
        bars
    )
    if rates is not None and len(rates):  
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop('real_volume', axis=1, inplace=True)
        return df
    else:
        print("NO rates found!")