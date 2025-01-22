# import numpy as np

# num_subchannels = 6
# sliding_window_size = 10
# resource_map = np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8)
# subframe_position = 4
# # Example: Add some values to simulate data
# resource_map[0, :] = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1]
# resource_map[1, :] = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1]
# resource_map[2, :] = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1]
# resource_map[4, :] = [0, 1, 0, 1, 0, 1, 1, 1, 1, 1]
# resource_map[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# resource_map[5, :] = [0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
# # Initialize a list to store results for each row

# mask = (resource_map[:,:subframe_position - 1] == 1)

# busy_indices = np.where(mask == 1)[0]
# print(busy_indices)

# import numpy as np

# num_subchannels = 6
# sliding_window_size = 10
# resource_map = np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8)
# subframe_position = 5
# # Example: Add some values to simulate data
# resource_map[0, :] = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1]
# resource_map[1, :] = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1]
# resource_map[2, :] = [0, 1, 0, 1, 2, 3, 1, 0, 0, 1]
# resource_map[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# resource_map[4, :] = [0, 1, 0, 1, 0, 1, 1, 1, 1, 1]
# resource_map[5, :] = [0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
# # Initialize a list to store results for each row

# # Rearrange resource_map based on subframe_position
# left_part = resource_map[:, :subframe_position]  # Columns from 0 to subframe_position (exclusive)
# right_part = resource_map[:, subframe_position:]  # Columns from subframe_position to end
# reordered_resource_map = np.hstack((right_part, left_part))  # Concatenate right part first, then left part
# # Reverse the sliced array along the columns
# reversed_map = reordered_resource_map[:, ::-1]
# # Compute cumulative product along the columns for all rows
# cumulative_mask = np.cumprod(reversed_map == 1, axis=1)
# # Count the valid continuous `1`s along each row
# continuous_ones = np.sum(cumulative_mask, axis=1)
# # Get the indices of busy subchannels
# busy_indices = np.where(continuous_ones > 0)[0]

# print(resource_map)
# print(reordered_resource_map)
# print(reversed_map)
# print(cumulative_mask)
# print(continuous_ones)
# print(busy_indices)

# # Output results
# print("Original Resource Map:")
# print(resource_map)
# print("\nReordered Resource Map (Older time on the left):")
# print(reordered_resource_map)
# print("\nReversed Map:")
# print(reversed_map)
# print("\nCumulative Mask:")
# print(cumulative_mask)
# print("\nContinuous Ones per Row:")
# print(continuous_ones)
# print("\nBusy Indices:")
# print(busy_indices)

# positions = []
# for i in range(10,59,10):
#     left_vehicle = i - 1  
#     right_vehicle = i
#     positions.append((left_vehicle, right_vehicle))
# print(positions)

# # Example dictionary from the image
# final_transmission = {
#     0: [1, 2, 3],
#     1: [],
#     2: [],
#     4: [],
#     5: [8],
#     3: [0, 1, 2],
#     6: [8, 9, 7],
#     7: [4, 5, 6, 8, 9],
#     8: [5, 6, 7, 9],
#     9: [6, 7, 8]
# }

# # Keys to extract
# target_keys = [6, 8]

# # Filter the dictionary to only include the target keys
# filtered_dict = {key: final_transmission[key] for key in target_keys if key in final_transmission} 
# success_num_central_five = sum(len(value) for value in filtered_dict.values())
# print("Filtered dictionary:", filtered_dict)
# print(success_num_central_five)



# import numpy as np

# # Example data
# continuous_ones = np.array([0, 3, 1, 5, 8, 2, 7, 4, 6, 9,10,12,6,7,8,2,1,4,5,6,7,3,1,5,6,6])  # Example computed values
# num_indices_to_include = int(len(continuous_ones) * 0.7)  # Calculate 70% of the total

# # Get the indices that would sort the array
# sorted_indices = np.argsort(continuous_ones)

# # Select the smallest 70% indices
# smallest_70_percent_indices = sorted_indices[:num_indices_to_include]

# print("Original continuous_ones:", continuous_ones)
# print("Sorted indices:", sorted_indices)
# print("Smallest 70% indices:", smallest_70_percent_indices)
# print("Values of smallest 70%:", continuous_ones[smallest_70_percent_indices])

# ## the first para is number of attackers, the second para is the distance between attackers
# import attacker_function as at
# import numpy as np
# attacker_positions = at.generate_attacker_position_pile()
# num_attackers = 18

specific_vehicles = [35,36]  # The vehicle ID you want to filter for
attempted_transmissions = {
    1: [33, 34, 35],
    2: [35, 36, 37],
    3: [38, 39, 40]
}
for channel, neighbors in attempted_transmissions.items():
    # Check if any specific vehicle is in the neighbors
    if any(vehicle in neighbors for vehicle in specific_vehicles):
        print(f"Channel {channel}: {neighbors}")