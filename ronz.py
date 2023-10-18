import pandas as pd
import matplotlib.pyplot as plt
import math

canard_ronz_df = pd.read_excel('ronz_canard.xlsx')
canard_x_list = []
canard_y_list = []
for index, row in canard_ronz_df.iterrows():
    xy = row['X']
    x, y = xy.split(' ')
    canard_x_list.append(x)
    canard_y_list.append(y)
canard_ronz_df = pd.DataFrame({'X': canard_x_list, 'Y': canard_y_list})
canard_ronz_df = canard_ronz_df.astype(float)

elevator_ronz_df = pd.read_excel('ronz_elevator.xlsx')
elevator_x_list = []
elevator_y_list = []
for index, row in elevator_ronz_df.iterrows():
    xy = row['X']
    x, y = xy.split(' ')
    elevator_x_list.append(x)
    elevator_y_list.append(y)
elevator_ronz_df = pd.DataFrame({'X': elevator_x_list, 'Y': elevator_y_list})
elevator_ronz_df = elevator_ronz_df.astype(float)


# Original chord length (1 unit)
original_chord_length = 1.0
# Desired chord length (455 units)
desired_chord_length = 455.0
# Scaling factor
scale_factor = desired_chord_length / original_chord_length
# Calculate the rotation angle in radians (5 degrees)
rotation_angle = math.radians(-5)
# Define the rotation point (leading edge)
rotation_point_x = 0.0
rotation_point_y = 0.0


# Apply scaling
canard_ronz_df['X'] *= scale_factor
canard_ronz_df['Y'] *= scale_factor
canard_ronz_df['X'] *= 0.9  # Think about this!
canard_ronz_df['Y'] *= 0.77
# Apply scaling
elevator_ronz_df['X'] *= scale_factor
elevator_ronz_df['Y'] *= scale_factor
elevator_ronz_df['X'] *= 0.9  # Think about this!
elevator_ronz_df['X'] *= 1.25
elevator_ronz_df['Y'] *= 0.70

# Apply X displacement to elevator df
elevator_trailing_x = elevator_ronz_df['X'].max()
elevator_x_displacement = desired_chord_length - elevator_trailing_x
elevator_ronz_df['X'] += elevator_x_displacement

# Apply the rotation to the X and Y coordinates
canard_ronz_df['X'], canard_ronz_df['Y'] = (
    (canard_ronz_df['X'] - rotation_point_x) * math.cos(rotation_angle) - (canard_ronz_df['Y'] - rotation_point_y) * math.sin(rotation_angle) + rotation_point_x,
    (canard_ronz_df['X'] - rotation_point_x) * math.sin(rotation_angle) + (canard_ronz_df['Y'] - rotation_point_y) * math.cos(rotation_angle) + rotation_point_y
)
# Apply the rotation to the X and Y coordinates
elevator_ronz_df['X'], elevator_ronz_df['Y'] = (
    (elevator_ronz_df['X'] - rotation_point_x) * math.cos(rotation_angle) - (elevator_ronz_df['Y'] - rotation_point_y) * math.sin(rotation_angle) + rotation_point_x,
    (elevator_ronz_df['X'] - rotation_point_x) * math.sin(rotation_angle) + (elevator_ronz_df['Y'] - rotation_point_y) * math.cos(rotation_angle) + rotation_point_y
)

ronz_df = pd.concat([canard_ronz_df, elevator_ronz_df], axis=0)

# ronz_df.to_pickle('ronz_df.pkl')
canard_ronz_df.to_excel('canard_ronz_df.xlsx')
elevator_ronz_df.to_excel('elevator_ronz_df.xlsx')

# plt.scatter(ronz_df['X'], ronz_df['Y'])
# # plt.scatter(elevator_ronz_df['X'], elevator_ronz_df['Y'])
# plt.axis('equal')
# plt.show()


pass

pass
