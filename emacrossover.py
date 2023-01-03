# Import necessary libraries
import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('AMARAJABAT.csv')

# Calculate the EMAs
data['ema_short'] = data['Close'].ewm(span=5, adjust=False).mean()
data['ema_mid'] = data['Close'].ewm(span=21, adjust=False).mean()
data['ema_long'] = data['Close'].ewm(span=55, adjust=False).mean()

# Initialize the strategy
data['strategy'] = np.nan

# Set the buy and sell signals
data.loc[data['ema_short'] > data['ema_long'], 'strategy'] = 1
data.loc[data['ema_short'] < data['ema_long'], 'strategy'] = -1

# Calculate the returns
data['returns'] = data['Close'].pct_change()

# Calculate the strategy returns
data['strategy_returns'] = data['returns'] * data['strategy'].shift(1)

# Print the strategy returns
print(data['strategy_returns'])

