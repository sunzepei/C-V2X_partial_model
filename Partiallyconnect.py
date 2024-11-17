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
# Simulation parameters
num_vehicles = 10
communication_range = 3 # Number of vehicles ahead and behind within communication range
num_subchannels = 15
num_subframes = 30000000
sps_interval_range = (2,7)
sliding_window_size = 10

# Variables to store PRR values
prr_values = []
threshold = 3

# Initialize vehicle information
vehicles_info = {}
for vehicle in range(num_vehicles):
    # Define each vehicle's neighbor range based on the communication range
    start_idx = max(0, vehicle - communication_range)
    end_idx = min(num_vehicles - 1, vehicle + communication_range)
    neighbors = list(range(start_idx, end_idx + 1))
    # neighbors.remove(vehicle)  # Exclude self

    vehicles_info[vehicle] = {
        'neighbors': neighbors,
        'current_subchannel': np.random.choice(num_subchannels),
        'next_selection_frame': 0,
        'sps_counter': np.random.randint(*sps_interval_range),
        # Local resource map for the last 10 subframes sliding window
        'resource_map': np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8)  
        }

total_neighbors = sum(len(info['neighbors']) for info in vehicles_info.values()) - num_vehicles


# Main simulation loop
for subframe in tqdm(range(num_subframes), desc="Processing", ncols=100):
    # Step 1: Allocate subchannels for vehicles and populate attempted transmissions
    attempted_transmissions = {}  # Track subchannel usage in the current subframe

    # Allocate subchannels and populate attempted_transmissions
    for vehicle, info in vehicles_info.items():
         # Handle SPS counter and reselection
        if subframe == info['next_selection_frame']:
            if info['sps_counter'] == 0:
                # Randomly reselect subchannel if the interval has elapsed
                info['current_subchannel'] = f.select_least_used_subchannel(subframe,info['current_subchannel'],
                                                                                info['resource_map'], threshold)
                f.update_neighbors(vehicle, info['current_subchannel'], vehicles_info)
                info['sps_interval'] = np.random.randint(sps_interval_range)
            else:
                pass
            info['sps_counter'] -= 1
            info['next_selection_frame'] = subframe + 1


       # Track attempted transmissions
        current_channel = info['current_subchannel']
        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(vehicle)

    transmissions = f.package_received(attempted_transmissions)
    success_num = sum(len(value) for value in transmissions.values())

    # Step 3: Calculate Packet Delivery Ratio (PDR) every 2000 subframes
    if subframe % 200 == 0:
        prr = f.calculate_PRR(success_num, total_neighbors)
        prr_values.append(prr)
    
    # print(attempted_transmissions)
    # print(total_successful_transmissions)


# Plot PDR over time
plt.figure(figsize=(10, 6))
plt.plot(range(0, num_subframes, 2000), prr_values, label='PDR over Time')
plt.xlabel('Subframe')
plt.ylabel('Packet Delivery Ratio (PDR)')
plt.title('PDR Trend Over Time')
plt.legend()
plt.grid(True)
plt.show()