import numpy as np




def choose_subchannel(vehicle, resource_map):
    """
    Choose a subchannel for the vehicle based on its local resource map.
    For simplicity, choose the least used subchannel.
    """
    subchannel_usage = np.sum(resource_map, axis=1)  # Sum usage across the sliding window
    least_used_subchannels = np.where(subchannel_usage == np.min(subchannel_usage))[0]
    return np.random.choice(least_used_subchannels)  # Pick randomly among the least used


def update_neighbors(vehicle, subchannel, vehicles_info):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    for neighbor in vehicles_info[vehicle]['neighbors']:
        # Shift the sliding window to make room for the latest subframe
        vehicles_info[neighbor]['resource_map'][:, :-1] = vehicles_info[neighbor]['resource_map'][:, 1:]
        # Mark the chosen subchannel as used in the latest subframe
        vehicles_info[neighbor]['resource_map'][subchannel, -1] = 1