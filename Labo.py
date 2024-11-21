import numpy as np
from fractions import Fraction
 # Function to pick subchannels with usage below a certain threshold
def pick_value_least(value_array, threshold):
  
    n = len(value_array)

    # Filtering values and indices
    indices = np.where(value_array <= threshold)[0].tolist()
    percent = len(indices) / n

    # Adjust the threshold until at least 20% of subchannels are below it
    while percent <= 0.2:
        threshold += 1
        indices = np.where(value_array <= threshold)[0].tolist()
        percent = len(indices) / n
    return indices



def choose_subchannel(current_subchannel,resource_map,threshold):
    """
    Choose a subchannel for the vehicle based on its local resource map.
    For simplicity, choose the least used subchannel.
    """
    indice = pick_value_least(resource_map,threshold)
    if current_subchannel in indice:
        indice.remove(current_subchannel)
    return np.random.choice(indice) # Pick randomly among the least used


def update_neighbors(vehicle, subchannel, vehicles_info,):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    for neighbor in vehicles_info[vehicle]['neighbors']:
        vehicles_info[neighbor]['resource_map'][subchannel] = 0.7*vehicles_info[neighbor]['resource_map'][subchannel] + 1

def package_received(attempt_transmission,successful_transmissions,station_info):
    for channel, vehicles in attempt_transmission.items():
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

def calculate_PRR(success_num, total_neighbors):
    return Fraction(success_num, total_neighbors)
