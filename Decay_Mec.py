import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import Labo as l
# Simulation parameters
num_vehicles = 70
communication_range = 5 # Number of vehicles ahead and behind within communication range
num_subchannels = 100
num_subframes = 30000
sps_interval_range = (2,7)
counting_interval = 10000
reselection_probability = 0.2
# Variables to store PRR values
prr_values = []
cumualtive_prr_value = []
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
        'resource_map':np.zeros(num_subchannels, dtype=np.uint8) 
        }


total_neighbors = sum(len(info['neighbors']) for info in vehicles_info.values()) - num_vehicles


# Main simulation loop
for subframe in tqdm(range(num_subframes), desc="Processing", ncols=100):
    # Step 1: Allocate subchannels for vehicles and populate attempted transmissions
    attempted_transmissions = {}  # Track subchannel usage in the current subframe
    successful_transmissions = {}  # Track successful transmissions in the current subframe
    # Allocate subchannels and populate attempted_transmissions
    for vehicle, info in vehicles_info.items():
        # print(f"Now is processing vehicle {vehicle}")
         # Handle SPS counter and reselection
        if subframe == info['next_selection_frame']:
            if info['sps_counter'] <= 0:
                if np.random.rand() < reselection_probability:
                # Randomly reselect subchannel if the interval has elapsed
                    info['current_subchannel'] = l.choose_subchannel(info['current_subchannel'],
                                                                            info['resource_map'],threshold)
                info['sps_counter'] = np.random.randint(sps_interval_range[0], sps_interval_range[1])
            else:
                pass

            l.update_neighbors(vehicle, info['current_subchannel'], vehicles_info)
            info['sps_counter'] -= 1
            # print(f"the {vehicle} counter is {info['sps_counter']}")
            info['next_selection_frame'] = subframe + 1

       # Track attempted transmissions
        current_channel = info['current_subchannel']
        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(vehicle)

    transmissions = l.package_received(attempted_transmissions,successful_transmissions,vehicles_info)
    success_num = sum(len(value) for value in transmissions.values())

    # Step 3: Calculate Packet Delivery Ratio (PDR) every 2000 subframes
    if subframe % counting_interval == 0:
        prr = l.calculate_PRR(success_num, total_neighbors)
        prr_values.append(prr)
        cumulative_prr = sum(prr_values) / len(prr_values)
        cumualtive_prr_value.append(cumulative_prr)
    # print(attempted_transmissions)
    # print(total_successful_transmissions)
for vehicle, info in vehicles_info.items():
    print(f"Vehicle {vehicle} Resource Map: {info['resource_map']}")
    print("------------------------------------------------------------")


# print(prr_values)
# Plot PDR over time
plt.figure(figsize=(10, 6))
plt.plot(cumualtive_prr_value, label='PRR over Time')
plt.xlabel('Number of PRR values')
plt.ylabel('Packet Received Ratio (PRR)')
plt.title('PRR Trend Over Time')
plt.legend()
plt.grid(True)
plt.show()