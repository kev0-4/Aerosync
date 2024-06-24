import pandas as pd

df = pd.read_csv('airport_codes.csv')

df = df.drop(['Country', 'Airport'], axis=1)

df.to_csv('airport_codes1.txt', index=False)