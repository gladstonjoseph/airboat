import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt

station = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
position = [1.083, 1.060, 1.035, 0.989, 0.962, 0.904, 0.843, 0.776, 0.750, 0.660, 0.591, 0.499, 0.400, 0.301, 0.189, 0.157, 0.078, 0.056]
top = [0.277, 0.231, 0.206, 0.182, 0.172, 0.157, 0.150, 0.147, 0.148, 0.151, 0.157, 0.165, 0.176, 0.189, 0.208, 0.213, 0.228, 0.233]
bottom = [0.333, 0.300, 0.292, 0.287, 0.286, 0.283, 0.283, 0.283, 0.282, 0.283, 0.287, 0.291, 0.299, 0.310, 0.327, 0.327, 0.337, 0.340]

# position_a = [1.237, 1.168, 1.102, 1.055, 0.973, 0.919, 0.817, 0.619, 0.243, 0.202]
# top_a = [0.266, 0.202, 0.170, 0.159, 0.147, 0.146, 0.147, 0.166, 0.222, 0.230]
# bottom_a = [0.299, 0.267, 0.257, 0.253, 0.249, 0.246, 0.246, 0.252, 0.289, 0.293]

canard_dim_df = pd.DataFrame({'Station': station,
                              'Position': position,
                              'Top': top,
                              'Bottom': bottom})

# canard_dim_df = pd.read_excel('Canard_Dimensions.xlsx')

# Convert from meters to mm
canard_dim_df[['Position', 'Top', 'Bottom']] = canard_dim_df[['Position', 'Top', 'Bottom']].multiply(1000)

canard_dim_df['Thickness'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Bottom'])
canard_dim_df['Y_top'] = 600 - canard_dim_df['Top']
canard_dim_df['Y_bottom'] = 600 - (canard_dim_df['Top'] + canard_dim_df['Thickness'])
canard_dim_df['Position'] = 1083 - canard_dim_df['Position']

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

canard_df['Y'] = canard_df['Y'] + 0  # Trying to coincide with gu255118_df

gu255118_df = pd.read_csv('e1230-il_tip.csv', skiprows=8)
gu255118_df = gu255118_df.drop(range(94 + 1, len(gu255118_df)), axis=0)
gu255118_df = gu255118_df.rename(columns={'X(mm)': 'X', 'Y(mm)': 'Y'})
gu255118_df = gu255118_df.astype(float)

# Ronz
# ronz_df = pd.read_pickle('ronz_df.pkl')

# Plot canard
plt.scatter(canard_df['X'], canard_df['Y'])
plt.plot(canard_df['X'], canard_df['Y'], label='Mid_Wing')

# Plot gu255118_df
# plt.plot(gu255118_df['X'], gu255118_df['Y'], label='Eppler 1230\nThickness: 90%\nPitch: -2.5°\nChord: 794mm')

# Ronz
# plt.scatter(ronz_df['X'], ronz_df['Y'], color='green', s=7, label='Roncz R1145MS')

# Set the aspect ratio to be equal
plt.axis('equal')
# Annotate each data point with its 'Station' value
for index, row in canard_dim_df.iterrows():
    plt.annotate(str(row['Station']), (row['Position'], row['Y_top']), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Mid Wing')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.legend()
plt.show()


pass
