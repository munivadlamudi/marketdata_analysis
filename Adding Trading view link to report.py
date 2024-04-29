import pandas as pd

# Load your existing report CSV file
report_file = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Reports_gen_multi_d25-08-2023.csv'
df = pd.read_csv(report_file)

# Define a function to concatenate the URL prefix with values from Column A
def generate_url(value):
    value_without_ns = value.replace('.NS', '')
    return 'https://in.tradingview.com/chart/jwaLOSvl/?symbol=NSE%3A' + str(value_without_ns)

# Apply the function to create a new column
df['URL'] = df['Stock Name'].apply(generate_url)

# Sort the DataFrame based on the 'Entry Date' column in descending order
df_sorted = df.sort_values(by='Entry Date', ascending=False)

# Save the sorted DataFrame to a new CSV file or overwrite the existing one
output_file = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Reports_gen_multi_d25-08-2023__Test_with_URL.csv'
df_sorted.to_csv(output_file, index=False)

print(f"New column 'URL' added and saved to {output_file}.")