import pandas as pd
data = {
    'product': ['SmartPhone', 'Laptop', 'SmartPhone', 'Desktop', 'Laptop'],
    'quantity': [10, 5, None, 7, 4],
    'revenue': [100, None, 30, 70, 40]
}
df = pd.DataFrame(data)
print("Original DataFrame:\n")
print(df)
NumericColumns = df.select_dtypes(include=['int64']).columns
df[NumericColumns] = df[NumericColumns].fillna(df[NumericColumns].mean())
print("\nDataFrame after filling missing values with column-wise means:\n")
print(df)
