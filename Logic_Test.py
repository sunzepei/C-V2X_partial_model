### Set union test
successful_transmissions = {
    5: [2, 3, 4],  # Vehicle 5 successfully transmitted to vehicles 2, 3, and 4
    8: [6, 7,3,11],     # Vehicle 8 successfully transmitted to vehicles 6 and 7
    12: [11,2,3,4]       # Vehicle 12 successfully transmitted to vehicle 11
}

inter_mediate = {key: set(value) for key, value in successful_transmissions.items()}

others_union = set().union(*(inter_mediate[other] for
                                 other in inter_mediate.keys()))
print(inter_mediate)
print(others_union)

# Data structure
# data = {
#     33: {neighbor: [] for neighbor in range(20)},  # 20 neighbors for transmitter 33
#     34: {neighbor: [] for neighbor in range(20)},  # 20 neighbors for transmitter 34
#     35: {neighbor: [] for neighbor in range(20)},  # 20 neighbors for transmitter 35
#     36: {neighbor: [] for neighbor in range(20)},  # 20 neighbors for transmitter 36
#     37: {neighbor: [] for neighbor in range(20)},  # 20 neighbors for transmitter 37
# }

# # Example: Add sub-frame data
# data[33][1].append(10)  # Neighbor 1 of transmitter 33 received at sub-frame 10
# data[33][1].append(12)  # Neighbor 1 of transmitter 33 received at sub-frame 12
# data[34][1].append(15)  # Neighbor 1 of transmitter 34 received at sub-frame 15

# neighbor_1_transmitter_33 = data[33][1]
