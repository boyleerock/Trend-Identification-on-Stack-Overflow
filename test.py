import pandas as pd
df = pd.read_csv("output/merge.csv")
df = df[df.frequency > 4]
print(df.head())