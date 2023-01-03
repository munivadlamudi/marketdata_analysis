import pandas as pd

def ema_crossover(df, fast_period, slow_period):
    # Calculate the fast and slow EMA
    df['fast_ema'] = df['Close'].ewm(span=fast_period).mean()
    df['slow_ema'] = df['Close'].ewm(span=slow_period).mean()
    
    # Create a 'position' column to hold the trade positions
    df['position'] = 0
    
    # Iterate through the rows of the dataframe
    for i, row in df.iterrows():
        # If the fast EMA crosses above the slow EMA, open a long position
        if (row['fast_ema'] > row['slow_ema']) and (df.loc[i-1, 'position'] != 1):
            df.loc[i, 'position'] = 1
        # If the fast EMA crosses below the slow EMA, close the position and go short
        elif (row['fast_ema'] < row['slow_ema']) and (df.loc[i-1, 'position'] != -1):
            df.loc[i, 'position'] = -1
        # Otherwise, maintain the current position
        else:
            df.loc[i, 'position'] = df.loc[i-1, 'position']
    
    return df

# Load the data into a Pandas dataframe
df = pd.read_csv('AMARAJABAT.csv')

# Apply the EMA crossover strategy
df = ema_crossover(df, fast_period=21, slow_period=55)

# View the resulting dataframe
print(df)
