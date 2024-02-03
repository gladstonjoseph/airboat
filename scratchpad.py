import pandas as pd


elevator_df = pd.read_excel('/Users/gladstonjoseph/Downloads/elevator_ronz_df.xlsx')
elevator_df = elevator_df.drop(columns=['Unnamed: 0'])
elevator_df.to_csv('/Users/gladstonjoseph/Downloads/elevator_ronz_df.csv')

pass