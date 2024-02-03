import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt

station = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
position = [1.836, 1.782, 1.670, 1.538, 1.417, 1.200, 0.972, 0.865, 0.710, 0.625]
top = [0.215, 0.185, 0.154, 0.144, 0.150, 0.170, 0.200, 0.217, 0.251, 0.251]
bottom = [0.269, 0.205, 0.196, 0.193, 0.193, 0.193, 0.282, 0.295, 0.315, 0.315]

position_a = [1.237, 1.168, 1.102, 1.055, 0.973, 0.919, 0.817, 0.619, 0.243, 0.202]
top_a = [0.266, 0.202, 0.170, 0.159, 0.147, 0.146, 0.147, 0.166, 0.222, 0.230]
bottom_a = [0.299, 0.267, 0.257, 0.253, 0.249, 0.246, 0.246, 0.252, 0.289, 0.293]

canard_dim_df = pd.DataFrame({'Station': station,
                              'Position': position_a,
                              'Top': top_a,
                              'Bottom': bottom_a})

# canard_dim_df = pd.read_excel('Canard_Dimensions.xlsx')

# Convert from meters to mm
canard_dim_df[['Position', 'Top', 'Bottom']] = canard_dim_df[['Position', 'Top', 'Bottom']].multiply(1000)

canard_dim_df['Thickness'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Bottom'])
canard_dim_df['Y_top'] = 600 - canard_dim_df['Top']
canard_dim_df['Y_bottom'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Thickness'])
canard_dim_df['Position'] = 1237 - canard_dim_df['Position']

# plt.plot(canard_dim_df['Position'], canard_dim_df['Y_top'])
# plt.plot(canard_dim_df['Position'], canard_dim_df['Y_bottom'])
# plt.axis('equal')
# plt.show()

# Fill the empty value for now
# canard_dim_df.loc[9, 'Position'] = 235
station_a = canard_dim_df[canard_dim_df['Position'] == 0]
point1_thickness_half = (station_a['Thickness'] / 2).squeeze()
y_offset = station_a['Y_top'].squeeze() - point1_thickness_half
canard_dim_df['Y_top'] = canard_dim_df['Y_top'] - y_offset
canard_dim_df['Y_bottom'] = canard_dim_df['Y_bottom'] - y_offset
canard_dim_df['Position'] = canard_dim_df['Position'] + 10  # Trying to coincide with gu255118_df

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

# Original chord length (1 unit)
original_chord_length = 1250
# Desired chord length (455 units)
desired_chord_length = 1279
# Scaling factor
scale_factor = desired_chord_length / original_chord_length
# Applying to df
canard_df['X'] *= scale_factor

canard_df['Y'] = canard_df['Y'] + 8  # Trying to coincide with gu255118_df

gu255118_df = pd.read_csv('e1230-il.csv', skiprows=8)
gu255118_df = gu255118_df.drop(range(94 + 1, len(gu255118_df)), axis=0)
gu255118_df = gu255118_df.rename(columns={'X(mm)': 'X', 'Y(mm)': 'Y'})
gu255118_df = gu255118_df.astype(float)

# Ronz
# ronz_df = pd.read_pickle('ronz_df.pkl')

# Plot canard
# plt.scatter(canard_df['X'], canard_df['Y'])
# plt.plot(canard_df['X'], canard_df['Y'], label='Wing')

# Plot gu255118_df
plt.plot(gu255118_df['X'], gu255118_df['Y'], label='Eppler 1230\nThickness: 95%\nPitch: 0°\nChord: 1279mm', linewidth=0.2)

# Ronz
# plt.scatter(ronz_df['X'], ronz_df['Y'], color='green', s=7, label='Roncz R1145MS')

# Set the aspect ratio to be equal
plt.axis('equal')
# # Annotate each data point with its 'Station' value
# for index, row in canard_dim_df.iterrows():
#     plt.annotate(str(row['Station']), (row['Position'], row['Y_top']), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Wing Dimensions (Data Points)')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.legend()
plt.show()


pass
