import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt


canard_dim_df = pd.read_excel('Canard_Dimensions.xlsx')

# Convert from meters to mm
canard_dim_df[['Position', 'Top', 'Bottom']] = canard_dim_df[['Position', 'Top', 'Bottom']].multiply(1000)

canard_dim_df['Thickness'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Bottom'])
canard_dim_df['Y_top'] = 600 - canard_dim_df['Top']
canard_dim_df['Y_bottom'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Thickness'])
canard_dim_df['Position'] = 447 - canard_dim_df['Position']
# Fill the empty value for now
canard_dim_df.loc[9, 'Position'] = 235
station_a = canard_dim_df[canard_dim_df['Position'] == 0]
point1_thickness_half = (station_a['Thickness'] / 2).squeeze()
y_offset = station_a['Y_top'].squeeze() - point1_thickness_half
canard_dim_df['Y_top'] = canard_dim_df['Y_top'] - y_offset
canard_dim_df['Y_bottom'] = canard_dim_df['Y_bottom'] - y_offset
canard_dim_df['Position'] = canard_dim_df['Position'] + 6  # Trying to coincide with gu255118_df

# Top Surface
canard_dim_df = canard_dim_df.sort_values(by='Position', ascending=False)
position_list_top = canard_dim_df['Position'].to_list()
y_list_top = canard_dim_df['Y_top'].to_list()

# Bottom Surface
canard_dim_df = canard_dim_df.sort_values(by='Position', ascending=True)
position_list_bottom = canard_dim_df['Position'].to_list()
y_list_bottom = canard_dim_df['Y_bottom'].to_list()

position_list = position_list_top + position_list_bottom
y_list = y_list_top + y_list_bottom

# position_list = canard_dim_df['Position'].to_list()
# position_list = position_list + position_list
# y_list = canard_dim_df['Y_top'].to_list() + canard_dim_df['Y_bottom'].to_list()

canard_df = pd.DataFrame({'X': position_list, 'Y': y_list})
canard_df['Y'] = canard_df['Y'] + 1  # Trying to coincide with gu255118_df

gu255118_df = pd.read_csv('gu255118-il.csv', skiprows=8)
gu255118_df = gu255118_df.drop(range(46 + 1, len(gu255118_df)), axis=0)
gu255118_df = gu255118_df.rename(columns={'X(mm)': 'X', 'Y(mm)': 'Y'})
gu255118_df = gu255118_df.astype(float)

# Ronz
ronz_df = pd.read_pickle('ronz_df.pkl')

# Plot canard
plt.scatter(canard_df['X'], canard_df['Y'])
plt.plot(canard_df['X'], canard_df['Y'], label='Canard')

# Plot gu255118_df
# plt.plot(gu255118_df['X'], gu255118_df['Y'], label='gu255118\nThickness: 75%\nPitch: 5.2°\nChord: 450mm')

# Ronz
plt.scatter(ronz_df['X'], ronz_df['Y'], color='green', s=7, label='Roncz R1145MS')

# Set the aspect ratio to be equal
plt.axis('equal')
# Annotate each data point with its 'Station' value
# for index, row in canard_dim_df.iterrows():
#     plt.annotate(str(row['Station']), (row['Position'], row['Y_top']), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Canard Dimensions (Data Points)')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.legend()
plt.show()


pass
