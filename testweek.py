import pandas as pd

df = pd.DataFrame(
	columns=["datetime"],
	data=pd.date_range("1-1-2023", periods=10, freq="D"))
print(df)

df["week_number"] = df["datetime"].dt.isocalendar().week
result = df.dtypes
print(result)
print(df)