# import pandas as pd

# # Read the CSV files into Pandas DataFrames
# df_a = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500/3MINDIA.NS.csv')
# df_b = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500_weekly/3MINDIA.NS_weekly.csv')

# # Merge DataFrames on the first condition: Column_A == Column_X
# merged_df = pd.merge(df_a, df_b, left_on='Year', right_on='Year', how='left')

# # Merge DataFrames on the second condition: Column_B == Column_Y
# merged_df = pd.merge(merged_df, df_b, left_on='week_number', right_on='week_number', how='left', suffixes=('_A', '_B'))

# # Update the values in "Column_C" with the values from "Column_Z"
# merged_df['cci34_1W'] = merged_df['cci34_1W'].combine_first(merged_df['cci34_1W'])

# # Drop the extra columns
# merged_df.drop(['Year', 'week_number', 'cci34_1W'], axis=1, inplace=True)

# # Save the updated DataFrame back to a new CSV file
# merged_df.to_csv('C:/Users/muniv/Desktop/Market/Compare/3MINDIA.NS.csv', index=False)



# import pandas as pd

# # Read the main CSV file
# main_df = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500/3MINDIA.NS.csv')

# # Read the weekly CSV file
# weekly_df = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500_weekly/3MINDIA.NS_weekly.csv')

# # Merge the main and weekly DataFrames based on 'year' and 'week_number'
# merged_df = pd.merge(main_df, weekly_df[['Actual_Year', 'week_number', 'cci34_1W']], on=['Actual_Year', 'week_number'], how='left')

# # Update the values in 'cci34_1W' column
# merged_df['cci34_1W_x'].fillna(merged_df['cci34_1W_y'], inplace=True)
# merged_df.drop(['cci34_1W_y', 'cci34_1W_x'], axis=1, inplace=True)
# merged_df.rename(columns={'cci34_1W_x': 'cci34_1W'}, inplace=True)

# # Save the updated DataFrame back to the main CSV file
# merged_df.to_csv('C:/Users/muniv/Desktop/Market/Compare/3MINDIA.NS.csv', index=False)





import pandas as pd

# Read the CSV files into Pandas DataFrames
main_df = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500/3MINDIA.NS.csv')
weekly_df = pd.read_csv('C:/Users/muniv/Desktop/Market/Nifty_All500_weekly/3MINDIA.NS_weekly.csv')

# Merge DataFrames based on the 'Actual_year' and 'week_number' columns
merged_df = pd.merge(main_df, weekly_df[['Actual_Year', 'week_number', 'cci34_1W']], 
                     left_on=['Actual_Year', 'week_number'], right_on=['Actual_Year', 'week_number'], 
                     how='left')

# Drop the extra columns and rename cci34_1W column
merged_df['cci34_1W'].fillna(merged_df['cci34_1W'], inplace=True)

# Save the updated DataFrame back to a new CSV file
merged_df.to_csv('C:/Users/muniv/Desktop/Market/Compare/3MINDIA.NS.csv', index=False)
