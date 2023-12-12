import pandas as pd

# read in csv file
df = pd.read_csv('quiz_scores.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# expand out participants list
df['Participants (number, office, charge out rate)'] = df['Participants (number, office, charge out rate)'].apply(lambda x: [item.strip() for item in x.split(';')])
df_expanded = df.explode('Participants (number, office, charge out rate)')

#  get counts, concatenate and make tidy
df_dummies = pd.get_dummies(df_expanded['Participants (number, office, charge out rate)'])
df_large = pd.concat([df_expanded, df_dummies], axis=1)
bool_columns = df_large.select_dtypes(include='bool').columns
df_names = df_large.groupby('Date')[bool_columns].sum().reset_index()
df_tidy = pd.merge(df, df_names, on='Date', how='left')

# drop irrelevant columns
cols_to_drop = ['Participants (number, office, charge out rate)', 'TBC', 'TBC with Keith', '', 'Unnamed: 10', "Can't remember"]
df_tidy = df_tidy.drop(columns=cols_to_drop)

print(df_tidy)
