import pandas as pd
df = pd.read_csv('sales_data.csv')  
print(df)
TotalRevenue = df.groupby('product')['revenue'].sum()
print(TotalRevenue)
