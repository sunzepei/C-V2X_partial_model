neighbor_sets = {0: {0,1, 2, 3}, 3: {0,1,2,3,4,5,6}, 5: {2,3,4,5,6,7,8},6:{9,3,4,5,6,11}}
sets = {key: set(value) for key, value in neighbor_sets.items()}

exclusive_neighbors = {}
for vehicle, neighbor_set in sets.items():
    # Union of neighbors of all other vehicles
    others_union = set().union(*(sets[other] for other in sets.keys() if other != vehicle))
    # Exclusive neighbors for the current vehicle
    unique_neighbors = neighbor_set - others_union
    exclusive_neighbors[vehicle] = list(unique_neighbors)

print("Exclusive neighbors:", exclusive_neighbors)