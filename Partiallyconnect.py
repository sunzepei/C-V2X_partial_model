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
communication_range_in_vehicles = 3 # Number of vehicles ahead and behind within communication range
num_subchannels = 15
num_subframes = 30000000
sps_interval_range = (2,7)
sliding_window_size = 10


# Counter for total successful transmissions
total_successful_transmissions = 0
pdr_values = []
threshold = 3
# Initialize vehicle information
vehicles_info = {}
for vehicle in range(num_vehicles):
    # Define each vehicle's neighbor range based on the communication range
    start_idx = max(0, vehicle - communication_range_in_vehicles)
    end_idx = min(num_vehicles - 1, vehicle + communication_range_in_vehicles)
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


# Function to update the resource map based on neighboring transmissions and collisions
def update_resource_maps(attempted_transmissions, failed_vehicles):
    for subchannel, vehicles in attempted_transmissions.items():
        # If there was a collision on this subchannel, mark as 2
        if any(vehicle in failed_vehicles for vehicle in vehicles):
            # Mark subchannel as 2 (collision) for each vehicle's neighbors
            for vehicle in vehicles:
                for neighbor in vehicles_info[vehicle]['neighbors']:
                    vehicles_info[neighbor]['resource_map'][subchannel] = 2
        else:
            # Mark subchannel as 1 (successful use) for each vehicle's neighbors
            for vehicle in vehicles:
                for neighbor in vehicles_info[vehicle]['neighbors']:
                    vehicles_info[neighbor]['resource_map'][subchannel] = 1

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
                info['sps_interval'] = np.random.randint(sps_interval_range)
    
            info['sps_counter'] -= 1
            info['next_selection_frame'] = subframe + 1


       # Track attempted transmissions
        current_channel = info['current_subchannel']
        if current_channel not in attempted_transmissions:
            attempted_transmissions[current_channel] = []
        attempted_transmissions[current_channel].append(vehicle)


    # Step 2: Detect collisions and count successful transmissions
    for subchannel, vehicles in attempted_transmissions.items():
        successful_vehicles = set()  # Vehicles that successfully transmitted
        failed_vehicles = set()  # Vehicles that encountered collisions

        # Check each vehicle for collisions with its neighbors
        for i in range(len(vehicles)):
            vehicle_i = vehicles[i]
            has_neighbor_collision = False

            for j in range(i + 1, len(vehicles)):
                vehicle_j = vehicles[j]
                
                # Check if vehicle_j is a neighbor of vehicle_i
                if vehicle_j in vehicles_info[vehicle_i]['neighbors']:
                    # Mark both vehicles as failed
                    has_neighbor_collision = True
                    failed_vehicles.add(vehicle_i)
                    failed_vehicles.add(vehicle_j)
                    # print(f"{vehicle_i} and {vehicle_j} are neighbors, marking both as failed")

            # If vehicle_i had no collisions with any neighbors, it succeeds
            if not has_neighbor_collision and vehicle_i not in failed_vehicles:
                successful_vehicles.add(vehicle_i)

        # Count all successful vehicles on this subchannel
        total_successful_transmissions += len(successful_vehicles)
    # Step 3: Update resource maps to reflect neighbor activity and collisions
    update_resource_maps(attempted_transmissions, failed_vehicles)

    # Step 3: Calculate Packet Delivery Ratio (PDR) every 2000 subframes
    if subframe % 2000 == 0:
        pdr = total_successful_transmissions / (num_vehicles * (subframe + 1))
        pdr_values.append(pdr)
    # print(attempted_transmissions)
    # print(total_successful_transmissions)


# Plot PDR over time
plt.figure(figsize=(10, 6))
plt.plot(range(0, num_subframes, 2000), pdr_values, label='PDR over Time')
plt.xlabel('Subframe')
plt.ylabel('Packet Delivery Ratio (PDR)')
plt.title('PDR Trend Over Time')
plt.legend()
plt.grid(True)
plt.show()