## This code simulate Partially connected vehicles environment
## The vehicle distance is 50m, number of vehicles is 70, the entire length is 3450m(equally placed)
## The communication range is 500m which is 10 vehicles
## Simulation loop is the same, sub-channel selection
## Only different is the collision detection part.
##



import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import function as f
from scipy.interpolate import interp1d
# Simulation parameters
num_vehicles = 70
communication_range = 10 # Number of vehicles ahead and behind within communication range
num_subchannels = 100
num_subframes = 2000000
sps_interval_range = (5,16)
sliding_window_size = 10
counting_interval = 1000
reselection_probability = 0.2
# Variables to store PRR values
prr_values = []
cumulative_prr_value = []
cumulative_prr_sum = 0
prr_count = 0
min_percent = 0.2
threshold = 3

# Initialize vehicle information
vehicles_info = {}
for vehicle in range(num_vehicles):
    # Define each vehicle's neighbor range based on the communication range
    start_idx = max(0, vehicle - communication_range)
    end_idx = min(num_vehicles - 1, vehicle + communication_range)
    neighbors = list(range(start_idx, end_idx + 1))
    # neighbors.remove(vehicle)  # Exclude self in the function already

    vehicles_info[vehicle] = {
        'neighbors': neighbors,
        'current_subchannel': np.random.choice(num_subchannels),
        'next_selection_frame': 0,
        'sps_counter': np.random.randint(sps_interval_range[0], sps_interval_range[1]),
        # Local resource map for the last 10 subframes sliding window
        'resource_map': np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8)
        }

# Initial the Storage of the data for vehicles
IPG_Storage = {
    33: {neighbor: [] for neighbor in range(23, 44)},  # Neighbors for transmitter 33 are 23 to 43
    34: {neighbor: [] for neighbor in range(24, 45)},  # Example: Neighbors for transmitter 34
    35: {neighbor: [] for neighbor in range(25, 46)},  # Example: Neighbors for transmitter 35
    36: {neighbor: [] for neighbor in range(26, 47)},  # Example: Neighbors for transmitter 36
    37: {neighbor: [] for neighbor in range(27, 48)},  # Example: Neighbors for transmitter 37
}

# for vehicle, info in vehicles_info.items():
#     print(f"Vehicle {vehicle} neighbors: {info['neighbors']}")

# for vehicle, info in vehicles_info.items():
#     print(f"Vehicle {vehicle} SPS_Counter: {info['sps_counter']}")




total_neighbors = sum(len(info['neighbors']) for info in vehicles_info.values()) - num_vehicles


# Main simulation loop
for subframe in tqdm(range(num_subframes), desc="Processing", ncols=100):
    # Step 1: Allocate subchannels for vehicles and populate attempted transmissions
    attempted_transmissions = {}  # Track subchannel usage in the current subframe
    successful_transmissions = {}  # Track successful transmissions in the current subframe
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
                    info['current_subchannel'] = f.choose_subchannel(info['current_subchannel'],
                                                                            info['resource_map'],threshold)
                info['sps_counter'] = np.random.randint(sps_interval_range[0], sps_interval_range[1])
            else:
                pass

            f.update_neighbors(vehicle, info['current_subchannel'], vehicles_info,subframe_position)
            info['sps_counter'] -= 1
            # print(f"the {vehicle} counter is {info['sps_counter']}")
            info['next_selection_frame'] = subframe + 1

       # Track attempted transmissions
        current_channel = info['current_subchannel']
        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(vehicle)

    transmissions = f.package_received(attempted_transmissions,successful_transmissions,vehicles_info)
    success_num = sum(len(value) for value in transmissions.values())

    # Step 3: Calculate Packet Delivery Ratio (PDR) every 2000 subframes
    if subframe % counting_interval == 0 and subframe != 0:
        prr = f.calculate_PRR(success_num, total_neighbors)
        cumulative_prr_sum += prr
        prr_count += 1
        cumulative_prr = cumulative_prr_sum / prr_count
        cumulative_prr_value.append(cumulative_prr)
    
    # print(attempted_transmissions)
    # print(transmissions)
    f.IPGModel_Berry(transmissions, IPG_Storage, subframe)

# for vehicle, info in vehicles_info.items():
#     print(f"Vehicle {vehicle} successful transmissions): {info['successful_transmissions']}")


ipg_data = f.calculate_IPG(IPG_Storage)
merged_list = f.merge_ipg_data(ipg_data)
unique_value, ccdf = f.calculate_IPG_tail(merged_list)
f.plot_IPG(unique_value, ccdf)
f.plot_PRR(cumulative_prr_value)
