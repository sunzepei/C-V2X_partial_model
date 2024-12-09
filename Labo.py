# import numpy as np
# from fractions import Fraction
#  # Function to pick subchannels with usage below a certain threshold
# def pick_value_least(value_array, threshold):
  
#     n = len(value_array)

#     # Filtering values and indices
#     indices = np.where(value_array <= threshold)[0].tolist()
#     percent = len(indices) / n

#     # Adjust the threshold until at least 20% of subchannels are below it
#     while percent <= 0.2:
#         threshold += 1
#         indices = np.where(value_array <= threshold)[0].tolist()
#         percent = len(indices) / n
#     return indices



# def choose_subchannel(current_subchannel,resource_map,threshold):
#     """
#     Choose a subchannel for the vehicle based on its local resource map.
#     For simplicity, choose the least used subchannel.
#     """
#     indice = pick_value_least(resource_map,threshold)
#     if current_subchannel in indice:
#         indice.remove(current_subchannel)
#     return np.random.choice(indice) # Pick randomly among the least used


# def update_neighbors(vehicle, subchannel, vehicles_info,):
#     """
#     Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
#     """
#     for neighbor in vehicles_info[vehicle]['neighbors']:
#         vehicles_info[neighbor]['resource_map'][subchannel] += 1

# def package_received(attempt_transmission,successful_transmissions,station_info):
#     for channel, vehicles in attempt_transmission.items():
#         if  len(vehicles) == 1:
#             vehicle = vehicles[0]
#             successful_transmissions[vehicle] = station_info[vehicle]['neighbors']
#         else:
#             all_neighbors = {}
#             for vehicle in vehicles:
#                 all_neighbors[vehicle] = station_info[vehicle]['neighbors']

#             sets = {key: set(value) for key, value in all_neighbors.items()}

#             # Find overlapping part (intersection of all sets)
#             exclusive_neighbors = {}
#             for vehicle, neighbor_set in sets.items():
#                     # Union of neighbors of all other vehicles
#                 others_union = set().union(*(sets[other] for
#                                  other in sets.keys() if other != vehicle))
#                 # Exclusive neighbors for the current vehicle
#                 unique_neighbors = neighbor_set - others_union
#                 exclusive_neighbors[vehicle] = list(unique_neighbors)
#                 successful_transmissions.update(exclusive_neighbors)
#     for key, values in successful_transmissions.items():
#         if key in values:
#             values.remove(key)  # This removes the vehicle from its neighbor list in place
#     return  successful_transmissions

# def calculate_PRR(success_num, total_neighbors):
#     return Fraction(success_num, total_neighbors)

# import numpy as np
# sliding_window_size = 10
# num_subchannels = 100
# sps_interval_range = (5,16)
# communication_range = 10
# num_vehicles = 70
# attacker_start_index = 70
# attacker_positions = [
#     (9, 10),
#     (19, 20),
#     (29, 30),
#     (39, 40),
#     (49, 50),
#     (59, 60)
# ]
# # Initialize vehicle information
# vehicles_info = {}
# for vehicle in range(num_vehicles):
#     # Define each vehicle's neighbor range based on the communication range
#     start_idx = max(0, vehicle - communication_range)
#     end_idx = min(num_vehicles - 1, vehicle + communication_range)
#     neighbors = list(range(start_idx, end_idx + 1))


#     # Insert attackers into the neighbor list where appropriate
#     for i, (left_vehicle, right_vehicle) in enumerate(attacker_positions):
#         attacker_idx = attacker_start_index + i
#         # If the neighbor range includes either 'left_vehicle' or 'right_vehicle',
#         # we consider the attacker as also in range.
#         if left_vehicle in neighbors and right_vehicle in neighbors:
#             neighbors.append(attacker_idx)

#     vehicles_info[vehicle] = {
#         'neighbors': neighbors,
#         'current_subchannel': np.random.choice(num_subchannels),
#         'next_selection_frame': 0,
#         'sps_counter': np.random.randint(sps_interval_range[0], sps_interval_range[1]),
#         # Local resource map for the last 10 subframes sliding window
#         'resource_map': np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8),
#         'last_update': 0,
#         }
    
# for vehicle,info in vehicles_info.items():
#     print(f"No. {vehicle}  {info['neighbors']}")


# num_attackers = 6
# communication_range = 10
# num_vehicles = 70
# for attackers in range(num_attackers):
#     start_idx = max(0, (attackers+1)*10 - communication_range)
#     end_idx = min(num_vehicles - 1, (attackers+1)*10 + communication_range)
#     neighbors = list(range(start_idx, end_idx + 1 if attackers == 5 else end_idx ))
#     print(neighbors)

transmissions = { 1: [1, 2, 3, 4, 5, 6, 7, 8, 70, 71],  2: [5, 6, 7, 8, 9, 74,75],  3:[5, 6, 7, 76,73, 9]}
attacker_idx = [70, 71, 72, 73, 74, 75]
for key, values in transmissions.items():
    for index in attacker_idx:
        if index in values:
            values.remove(index)
print(transmissions)