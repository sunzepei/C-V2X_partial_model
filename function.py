import numpy as np
from fractions import Fraction

#  # Function to pick subchannels with usage below a certain threshold
# def pick_value_least(value_list, threshold):
#     value_array = np.array(value_list)
#     n = len(value_list)

#     # Filtering values and indices
#     mask = value_array <= threshold
#     selected_values = value_array[mask].tolist()
#     indices = np.where(mask)[0].tolist()
#     num_selected = len(selected_values)
#     percent = num_selected / n

#     # Adjust the threshold until at least 20% of subchannels are below it
#     while percent <= 0.2:
#         threshold += 1
#         mask = value_array <= threshold
#         selected_values = value_array[mask].tolist()
#         indices = np.where(mask)[0].tolist()
#         num_selected = len(selected_values)
#         percent = num_selected / n

#     return indices

 # advanced Function to pick subchannels with usage below a certain threshold
def pick_value_least(value_list, min_percent):
    value_array = np.array(value_list)
    n = len(value_list)
    threshold = np.percentile(value_array, min_percent * 100)
    indices = np.where(value_array <= threshold)[0].tolist()
    return indices

def choose_subchannel(current_subchannel,resource_map,threshold):
    """
    Choose a subchannel for the vehicle based on its local resource map.
    For simplicity, choose the least used subchannel.
    """
    subchannel_usage = np.sum(resource_map[:, :] > 0, axis=1)
    indice = pick_value_least(subchannel_usage, threshold)
    if current_subchannel in indice:
        indice.remove(current_subchannel)
    return np.random.choice(indice) # Pick randomly among the least used


def update_neighbors(vehicle, subchannel, vehicles_info,current_subframe, sliding_window_size):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    if current_subframe < sliding_window_size:
        # Directly update the column corresponding to the current sub-frame
        for neighbor in vehicles_info[vehicle]['neighbors']:
            vehicles_info[neighbor]['resource_map'][:, current_subframe] = 0  # Reset current sub-frame
            vehicles_info[neighbor]['resource_map'][subchannel, current_subframe] = 1  # Mark usage
    else:
        for neighbor in vehicles_info[vehicle]['neighbors']:
            vehicles_info[neighbor]['resource_map'][:, :-1] = vehicles_info[neighbor]['resource_map'][:, 1:]
            vehicles_info[neighbor]['resource_map'][subchannel, -1] = 1


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