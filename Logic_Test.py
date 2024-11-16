import random

# Constants
NUM_STATIONS = 10      # Number of communication stations
COMRANGE= 3         # Communication radius (3 neighbors on each side)
NUM_CHANNELS = 12     # Available channels
from fractions import Fraction

station_info = {}

for vehicle in range(NUM_STATIONS):
    start_idx = max(0, vehicle - COMRANGE)
    end_idx = min(NUM_STATIONS - 1, vehicle + COMRANGE)
    # print(end_idx)
    neighbors = list(range(start_idx, end_idx + 1))

    station_info[vehicle] = {
        'neighbors': neighbors,
        'subchannel': random.randint(1, NUM_CHANNELS)
    }

# Print out the neighbors for each station
for station, info in station_info.items():
    print(f"Station {station} neighbors: {info['neighbors']}")

total_neighbors = sum(len(info['neighbors']) for info in station_info.values()) - NUM_STATIONS

attempted_transmissions = {}


# Track attempted transmissions by each vehicle
for vehicle, info in station_info.items():
    current_channel = info['subchannel']
    if current_channel not in attempted_transmissions:
        attempted_transmissions[current_channel] = []
    attempted_transmissions[current_channel].append(vehicle)

print("Attempted transmissions:", attempted_transmissions)


successful_transmissions = {}

def package_received(vehicle_transmission):
    for channel, vehicles in vehicle_transmission.items():
        if  len(vehicles) == 1:
            vehicle = vehicles[0]
            successful_transmissions[vehicle] = station_info[vehicle]['neighbors']
        else:
            all_neighbors = {}
            for vehicle in vehicles:
                all_neighbors[vehicle] = station_info[vehicle]['neighbors']

            sets = {key: set(value) for key, value in all_neighbors.items()}

            # Find overlapping part (intersection of all sets)
            exclusive_neighbors = {}
            for vehicle, neighbor_set in sets.items():
                    # Union of neighbors of all other vehicles
                others_union = set().union(*(sets[other] for
                                 other in sets.keys() if other != vehicle))
                # Exclusive neighbors for the current vehicle
                unique_neighbors = neighbor_set - others_union
                exclusive_neighbors[vehicle] = list(unique_neighbors)
                successful_transmissions.update(exclusive_neighbors)
    for key, values in successful_transmissions.items():
        if key in values:
            values.remove(key)  # This removes the vehicle from its neighbor list in place
    return  successful_transmissions

transmissions = package_received(attempted_transmissions)
print(f"The final transmissioj is{transmissions},\n")
success_num = sum(len(value) for value in transmissions.values())

print(Fraction(success_num, total_neighbors))
