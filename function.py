import numpy as np
from fractions import Fraction
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
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

#  # advanced Function to pick subchannels with usage below a certain threshold
# def pick_value_least(value_list, min_percent,threshold):
#     value_array = np.array(value_list)
#     indices = np.where(value_array <= threshold)[0].tolist()
#     if len(indices) < min_percent * len(value_list):
#         new_threshold = np.percentile(value_array, min_percent * 100)
#         indices = np.where(value_array <= new_threshold)[0].tolist()
#     return indices


def choose_subchannel(current_subchannel,resource_map,threshold):
    """
    Choose a subchannel for the vehicle based on its local resource map.
    For simplicity, choose the least used subchannel.
    """
    subchannel_usage = np.sum(resource_map[:, :], axis=1)
    indice = pick_value_least(subchannel_usage,threshold)
    if current_subchannel in indice:
        indice.remove(current_subchannel)
    return np.random.choice(indice) # Pick randomly among the least used


def update_neighbors(vehicle, subchannel, vehicles_info,subframe_position):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    for neighbor in vehicles_info[vehicle]['neighbors']:
        vehicles_info[neighbor]['resource_map'][subchannel, subframe_position] = 1  # Mark usage



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

def store_IPG(transmissions, vehicles_info,subframe):
    inter_mediate = {key: set(value) for key, value in transmissions.items()}
    others_union = set().union(*(inter_mediate[other] for
                                other in inter_mediate.keys()))
    for  vehicles in others_union:
        vehicles_info[vehicles][ 'successful_transmissions'].append(subframe)



def IPGModel_Berry(transmissions,IPG_Storage , subframe):
    vehicles = [33, 34, 35, 36, 37]
    for vehicle in vehicles:
        neighbors = transmissions[vehicle]
        for neighbor in neighbors:
            IPG_Storage[vehicle][neighbor].append(subframe)



def calculate_IPG(IPG_Storage):
    ipg_data = {}
    # Calculate IPG for each vehicle
    for transmitter, neighbors in IPG_Storage.items():
        if transmitter not in ipg_data:
            ipg_data[transmitter] = {}
        for neighbor,sub_frame in neighbors.items():
            ipg_list = []
            for i in range(1, len(sub_frame)):
                ipg = sub_frame[i] - sub_frame[i - 1]
                ipg_list.append(ipg)
            ipg_data[transmitter][neighbor] = ipg_list
        # print(info['sps_counter'])
    return ipg_data

def merge_ipg_data(ipg_data):
    merged_list = []
    for transmitter, neighbors in ipg_data.items():
        for neighbor, ipg_list in neighbors.items():
            merged_list.extend(ipg_list)  # Add all elements from the IPG list
    return merged_list

def calculate_IPG_tail(ipg_list):
    # Calculate the CCDF for IPG
    ipg_array = np.array(ipg_list)
    ipg_100ms_prob = np.sum(ipg_array == 1) / len(ipg_array)
    ipg_sorted = np.sort(ipg_array) * 100  # Convert sub-frames to milliseconds (assuming 1 sub-frame = 100 ms)
    unique_value, counts = np.unique(ipg_sorted, return_counts= True)

    cdf = np.cumsum(counts)/len(ipg_sorted)
    ccdf = 1 - cdf
    target_ccdf = 10 ** -5
    interpolator = interp1d(ccdf, unique_value, fill_value="extrapolate")
    x_value_at_target_ccdf = interpolator(target_ccdf)
    print(f"X-axis value at CCDF = 10^-5 : {x_value_at_target_ccdf}")
    print("Probability of 100ms IPG:", ipg_100ms_prob)
    return unique_value, ccdf

def neighbor_values(vehicles_info,num_vehicles):
    sum_up = 0
    for vehicle, info in vehicles_info.items():
        sum_up = sum_up + len(info['neighbors'])
    print(f"the number of neighbor update is {sum_up - num_vehicles}")


# # Plotting the CCDF of IPG
def plot_IPG(unique_value, ccdf):
    plt.figure(figsize=(15, 8))
    plt.plot(unique_value, ccdf, label='CCDF of IPG')
    plt.xlabel('Inter-Packet Gap (IPG) [ms]')
    plt.ylabel('CCDF')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.title('CCDF of Inter-Packet Gap (IPG)')
    plt.legend()
    plt.grid(True)



def plot_PRR(cumulative_prr_value):
    # Plot PDR over time
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_prr_value, label='PRR over Time')
    plt.xlabel('Number of PRR values')
    plt.ylabel('Packet Received Ratio (PRR)')
    plt.title('PRR Trend Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

