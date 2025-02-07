## This code simulate Partially connected vehicles environment
## The vehicle distance is 50m, number of vehicles is 70, the entire length is 3450m(equally placed)
## The communication range is 500m which is 10 vehicles
## Simulation loop is the same, sub-channel selection
## Only different is the collision detection part.
##



import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import attacker_function as at
import pandas as pd
import random

# Set seed for reproducibility
seed = 42
random.seed(seed)  # Seed the built-in random module
np.random.seed(seed)  # Seed the NumPy random module


# Simulation parameters
num_vehicles = 70

communication_range = 10 # Number of vehicles ahead and behind within communication range
num_subchannels = 100
num_subframes = 2000000
sps_interval_range = (5,16)
sliding_window_size = 10
counting_interval = 1000
reselection_probability = 0.2
##Adding attackers
attacker_start_index = 70
# Variables to store PRR values
cumulative_prr_value = []
cumulative_prr_value_edge = []
cumulative_prr_value_central = []
cumulative_prr_sum = 0
cumulative_prr_sum_edge = 0
cumulative_prr_sum_central = 0
prr_count = 0
prr_count_dic = []
prr_count_central = 0
min_percent = 0.2
threshold = 3
vehicles_index_edge = [65, 66, 67, 68, 69]
vehicle_index_central = [33, 34, 35, 36, 37]
prr_count_edge = 0
## the first para is number of attackers, the second para is the distance between attackers
attacker_positions = at.generate_attacker_position_pile()
num_attackers = 6
attackers_info = {}

# Initialize attackers information
for attacker_id in range(num_vehicles, num_vehicles + num_attackers):
    # Cycle through attacker_positions using modulo
    left_vehicle, right_vehicle = attacker_positions[(attacker_id - num_vehicles) % len(attacker_positions)]
    
    # Calculate neighbors based on position and communication range
    start_idx = max(0, left_vehicle - communication_range)
    end_idx = min(num_vehicles - 1, right_vehicle + communication_range - 1)
    neighbors = list(range(start_idx, end_idx + 1))

    # Add attacker info
    attackers_info[attacker_id] = {
        'sps_interval': 10,  # Fixed SPS interval for all attackers
        'attack_subchannel': None,
        'next_attack_frame': 0,
        'neighbors': neighbors,
        'resource_map': np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8),
    }


# Initialize vehicle information
vehicles_info = {}
for vehicle in range(num_vehicles):
    # Define each vehicle's neighbor range based on the communication range
    start_idx = max(0, vehicle - communication_range)
    end_idx = min(num_vehicles - 1, vehicle + communication_range)
    neighbors = list(range(start_idx, end_idx + 1))
    # neighbors.remove(vehicle)  # Exclude self in the function already
    
        # Insert attackers into the neighbor list where appropriate
    for i in range(num_attackers):
        # Cycle through attacker_positions using modulo
        left_vehicle, right_vehicle = attacker_positions[i % len(attacker_positions)]
        attacker_idx = attacker_start_index + i

        # If the neighbor range includes either 'left_vehicle' or 'right_vehicle',
        # consider the attacker as a neighbor.
        if left_vehicle in neighbors and right_vehicle in neighbors:
            neighbors.append(attacker_idx)

    vehicles_info[vehicle] = {
        'neighbors': neighbors,
        'current_subchannel': np.random.choice(num_subchannels),
        'next_selection_frame': 0,
        'sps_counter': np.random.randint(sps_interval_range[0], sps_interval_range[1]),
        # Local resource map for the last 10 subframes sliding window
        'resource_map': np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8),
        }
number_attack_in_neighbors = 0
for vehicle, info in vehicles_info.items():
    number_attack_in_neighbors += sum(1 for neighbor in info['neighbors'] if neighbor >= attacker_start_index)
print(f"Number of attackers in neighbors: {number_attack_in_neighbors}")
total_neighbors = sum(len(info['neighbors']) for info in vehicles_info.values()) - num_vehicles - number_attack_in_neighbors
# Sum the number of neighbors for vehicles in vehicles_index
total_neighbors_edge = 60

# print(total_neighbors_edge)
# for vehicle, info in vehicles_info.items():
#     if vehicle in vehicles_index:
#         print(f"Vehicle {vehicle} neighbors: {info['neighbors']}"  )



# Initial the Storage of the data for vehicles
IPG_Storage = {
    65: {neighbor: [] for neighbor in range(55, 70) if neighbor != 65},  # Neighbors for transmitter 65 are 55 to 64
    66: {neighbor: [] for neighbor in range(56, 70) if neighbor != 66},  # Example: Neighbors for transmitter 66
    67: {neighbor: [] for neighbor in range(57, 70) if neighbor != 67},  # Example: Neighbors for transmitter 67
    68: {neighbor: [] for neighbor in range(58, 70) if neighbor != 68},  # Example: Neighbors for transmitter 68
    69: {neighbor: [] for neighbor in range(59, 70) if neighbor != 69},  # Example: Neighbors for transmitter 69
}

# Initial the Storage of the Latest Updated Subframe for vehicles
Last_update_Storage = {
    65: {neighbor: 0 for neighbor in range(55, 70) if neighbor != 65},  # Neighbors for transmitter 65 are 55 to 64
    66: {neighbor: 0 for neighbor in range(56, 70) if neighbor != 66},  # Example: Neighbors for transmitter 66
    67: {neighbor: 0 for neighbor in range(57, 70) if neighbor != 67},  # Example: Neighbors for transmitter 67
    68: {neighbor: 0 for neighbor in range(58, 70) if neighbor != 68},  # Example: Neighbors for transmitter 68
    69: {neighbor: 0 for neighbor in range(59, 70) if neighbor != 69},  # Example: Neighbors for transmitter 69
}

# Initial the Storage of the AOI for vehicles
AOI_Storage = {
    65: {neighbor: [] for neighbor in range(55, 70) if neighbor != 65},  # Neighbors for transmitter 65 are 55 to 64
    66: {neighbor: [] for neighbor in range(56, 70) if neighbor != 66},  # Example: Neighbors for transmitter 66
    67: {neighbor: [] for neighbor in range(57, 70) if neighbor != 67},  # Example: Neighbors for transmitter 67
    68: {neighbor: [] for neighbor in range(58, 70) if neighbor != 68},  # Example: Neighbors for transmitter 68
    69: {neighbor: [] for neighbor in range(59, 70) if neighbor != 69},  # Example: Neighbors for transmitter 69
}


# Main simulation loop
for subframe in tqdm(range(num_subframes), desc="Processing", ncols=100):
    # Step 1: Allocate subchannels for vehicles and populate attempted transmissions
    attempted_transmissions = {}  # Track subchannel usage in the current subframe
    vehicle_channel_pick = {} ## This stores the channel picked by the vehicle in each subframe
    attacker_channel_pick = {} ## This stores the channel picked by the attacker in each subframe
    # Allocate subchannels and populate attempted_transmissions
    subframe_position = subframe % sliding_window_size
    for vehicle in vehicles_info:
        vehicles_info[vehicle]['resource_map'][:, subframe_position] = 0  # Reset current sub-frame

    for vehicle, info in vehicles_info.items():
        # print(f"Now is processing vehicle {vehicle}")
         # Handle SPS counter and reselection
        if subframe == info['next_selection_frame']:
            if info['sps_counter'] <= 0:
                if np.random.rand() < reselection_probability:
                # Randomly reselrect subchannel if the interval has elapsed
                    info['current_subchannel'] = at.choose_subchannel(info['current_subchannel'],
                                                                            info['resource_map'],threshold)
                info['sps_counter'] = np.random.randint(sps_interval_range[0], sps_interval_range[1])

            vehicle_channel_pick[vehicle] = info['current_subchannel']
            info['sps_counter'] -= 1
            # print(f"the {vehicle} counter is {info['sps_counter']}")
            info['next_selection_frame'] = subframe + 1
            
       # Track attempted transmissions
        current_channel = info['current_subchannel']

        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(vehicle)

        # Mark the subchannel usage for attackers first
    for attacker_id, info in attackers_info.items():
        if subframe == info['next_attack_frame']:
            info['attack_subchannel'] = at.select_channel_to_attack(info['resource_map'],num_subchannels)
            info['next_attack_frame'] = subframe + info['sps_interval']
        current_channel = info['attack_subchannel']
        attacker_channel_pick[attacker_id] = current_channel

        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(attacker_id)

    at.update_vehicle_neighbors_row(vehicles_info,vehicle_channel_pick, subframe_position,attackers_info,attacker_start_index)
    at.update_attacker_neighbors_row(vehicles_info, attacker_channel_pick,subframe_position,attackers_info,attacker_start_index)
    transmissions = at.package_received(attempted_transmissions,vehicles_info,attacker_start_index,attackers_info,)


    ## If attacker is in successful transmission dictionary, remove it, casue vehicle can't trasmit to attacker
    for key, values in transmissions.items():
        for index in attackers_info.keys():
            if index in values:
                values.remove(index)
       
    success_num = sum(len(value) for value in transmissions.values())
    # Filter the dictionary to only include the target keys
    filtered_dict_edge = {key: transmissions[key] for key in vehicles_index_edge if key in transmissions}
    filtered_dict_central = {key: transmissions[key] for key in vehicle_index_central if key in transmissions}
    success_num_edge_five = sum(len(value) for value in filtered_dict_edge.values())
    success_num_central_five = sum(len(value) for value in filtered_dict_central.values())

   # Step 3: Calculate Packet Delivery Ratio (PRR)over all vehicles every 2000 subframes
    if subframe % counting_interval == 0 and subframe != 0:

        prr = at.calculate_PRR(success_num, total_neighbors)
        cumulative_prr_sum += prr
        prr_count += 1
        prr_count_dic.append(prr_count)
        cumulative_prr = cumulative_prr_sum / prr_count
        cumulative_prr_value.append(cumulative_prr)

    ## Calculate the edge 5 vehicles PRR every 2000 subframes
    if subframe % counting_interval == 0 and subframe != 0:

        prr_edge = at.calculate_PRR(success_num_edge_five, total_neighbors_edge)
        cumulative_prr_sum_edge += prr_edge
        prr_count_central += 1
        cumulative_prr_edge = cumulative_prr_sum_edge / prr_count_central
        cumulative_prr_value_edge.append(cumulative_prr_edge)

    ## Calculate the central 5 vehicles PRR every 2000 subframes
    if subframe % counting_interval == 0 and subframe != 0:
        prr_central = at.calculate_PRR(success_num_central_five,100)
        cumulative_prr_sum_central += prr_central
        prr_count_edge += 1
        cumulative_prr_central = cumulative_prr_sum_central /  prr_count_edge
        cumulative_prr_value_central.append(cumulative_prr_central)

    at.IPGModel_Berry(transmissions, IPG_Storage, subframe,vehicles_index_edge)
    at.AOI_last_update(Last_update_Storage,subframe,transmissions,vehicles_index_edge)
    at.AOI_model(Last_update_Storage,subframe,AOI_Storage)# for vehicle, info in vehicles_info.items():
#     print(f"Vehicle {vehicle} successful transmissions): {info['successful_transmissions']}")


ipg_data = at.calculate_IPG(IPG_Storage)
merged_ipg_list = at.merge_data(ipg_data)
unique_ipg_value,ipg_ccdf = at.calculate_ipg_tail(merged_ipg_list)

## problem here: the reason why AoI tail is too long cause i didn't count the vehicle itself it 
merge_aoi_list = at.merge_data(AOI_Storage)
unique_aoi_value, aoi_ccdf,num_count = at.calculate_aoi_tail(merge_aoi_list)


##Store the data of PRR
df = pd.DataFrame({
    "Key": prr_count_dic,
    "Value1": list(map(float,cumulative_prr_value)),
    "Value2": list(map(float,cumulative_prr_value_edge)),
    "Value3": list(map(float,cumulative_prr_value_central)),
})
df.to_csv("PRR_Storage.csv", index=False)
print("PRR Storage saved to 'PRR_Storage.xlsx'")


### store the data of AOI
# value_count_dict = dict(zip(unique_aoi_value,num_count))
# df = pd.DataFrame(value_count_dict.items(), columns=['AOI', 'Count'])
# df.to_csv("AOI_Storage.csv", index=False)
# print("AOI Storage saved to 'AOI_Storage.xlsx'")

at.plot_ipg_tail(unique_ipg_value, ipg_ccdf)
at.plot_aoi_tail(unique_aoi_value, aoi_ccdf)

at.plot_PRR(cumulative_prr_value)
at.plot_PRR(cumulative_prr_value_edge)
at.plot_PRR(cumulative_prr_value_central)

plt.show()
