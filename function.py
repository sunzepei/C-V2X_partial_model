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


# Function to select the least used subchannel based on historical usage
def select_least_used_subchannel(subframe, current_subchannel, resource_map,threshold):
    sensing_range_start = max(0, subframe - 10)
    subchannel_usage = np.sum(resource_map[:, sensing_range_start:subframe] > 0, axis=1)

    # Sort subchannels by usage, and get the indices of the sorted subchannels
    indice = pick_value_least(subchannel_usage, threshold)
    # exclude the same resource it is in
    if current_subchannel in indice:
        indice.remove(current_subchannel)

    return np.random.choice(indice)