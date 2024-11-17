import numpy as np


 # Function to pick subchannels with usage below a certain threshold
def pick_value_least(value_list, threshold):
    value_array = np.array(value_list)
    n = len(value_list)

    # Filtering values and indices
    mask = value_array <= threshold
    selected_values = value_array[mask].tolist()
    indices = np.where(mask)[0].tolist()
    num_selected = len(selected_values)
    percent = num_selected / n

    # Adjust the threshold until at least 20% of subchannels are below it
    while percent <= 0.2:
        threshold += 1
        mask = value_array <= threshold
        selected_values = value_array[mask].tolist()
        indices = np.where(mask)[0].tolist()
        num_selected = len(selected_values)
        percent = num_selected / n

    return indices

def choose_subchannel(vehicle, resource_map,threshold,current_subchannel):
    """
    Choose a subchannel for the vehicle based on its local resource map.
    For simplicity, choose the least used subchannel.
    """
    subchannel_usage = np.sum(resource_map[:, :] > 0, axis=1)
    indice = pick_value_least(subchannel_usage, threshold)
    if current_subchannel in indice:
        indice.remove(current_subchannel)
    return np.random.choice(indice) # Pick randomly among the least used


def update_neighbors(vehicle, subchannel, vehicles_info):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    for neighbor in vehicles_info[vehicle]['neighbors']:
        # Shift the sliding window to make room for the latest subframe
        vehicles_info[neighbor]['resource_map'][:, :-1] = vehicles_info[neighbor]['resource_map'][:, 1:]
        # Mark the chosen subchannel as used in the latest subframe
        vehicles_info[neighbor]['resource_map'][subchannel, -1] = 1