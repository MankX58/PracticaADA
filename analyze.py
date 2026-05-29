import pandas as pd
df = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
print(f'Total edges: {len(df)}')
unique_nodes = set(df['origin']).union(set(df['destination']))
print(f'Total unique nodes: {len(unique_nodes)}')
print(f'Rows with names: {len(df.dropna(subset=["name"]))}')
print(f'Unique names: {len(df["name"].dropna().unique())}')
