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


# Function to select a subchannel for attackers to attack
def select_channel_to_attack(resource_map,num_subchannels):
    subchannel_usage = np.sum(resource_map[:, :], axis= 1)
    busy_indices = np.where(subchannel_usage > 0)[0]
    return np.random.choice(busy_indices) if len(busy_indices) > 0 else np.random.choice(num_subchannels)


def update_neighbors(vehicle, subchannel, vehicles_info,subframe_position,attackrs_info,attacker_start_index):
    """
    Inform the neighbors of the vehicle's subchannel choice and update their resource maps.
    """
    for neighbor in vehicles_info[vehicle]['neighbors']:
        if neighbor < attacker_start_index:
            vehicles_info[neighbor]['resource_map'][subchannel, subframe_position] = 1  # Mark usage
        else:
            attackrs_info[neighbor]['resource_map'][subchannel, subframe_position] = 1

def update_neighbors_row(vehicle_info,channel_pick,subframe_position,attackrs_info,attacker_start_index):
    for vehicle, subchannel in channel_pick.items():
        if vehicle < attacker_start_index:
            for neighbor in vehicle_info[vehicle]['neighbors']:
                if neighbor < attacker_start_index:
                    vehicle_info[neighbor]['resource_map'][subchannel, subframe_position] = 1
                else:
                    attackrs_info[neighbor]['resource_map'][subchannel, subframe_position] = 1
        else:
            for neighbor in attackrs_info[vehicle]['neighbors']:
                if neighbor < attacker_start_index:
                    vehicle_info[neighbor]['resource_map'][subchannel, subframe_position] = 1
                else:
                    attackrs_info[neighbor]['resource_map'][subchannel, subframe_position] = 1

def package_received(attempt_transmission,station_info,attacker_start_index,attackers_info):
    successful_transmissions = {}
    for channel, vehicles in attempt_transmission.items():
        if  len(vehicles) == 1:
            if vehicles[0] < attacker_start_index:
                vehicle = vehicles[0]
                successful_transmissions[vehicle] = station_info[vehicle]['neighbors']
            else:
                pass
        else:     
            all_neighbors = {}
            for vehicle in vehicles:
                if vehicle < attacker_start_index:
                    all_neighbors[vehicle] = station_info[vehicle]['neighbors']
                else:
                    all_neighbors[vehicle] = attackers_info[vehicle]['neighbors']

            sets = {key: set(value) for key, value in all_neighbors.items()}

            # Find overlapping part (intersection of all sets)
            exclusive_neighbors = {}
            for vehicle, neighbor_set in sets.items():
                if vehicle < attacker_start_index:
                    # Union of neighbors of all other vehicles
                    others_union = set().union(*(sets[other] for
                                    other in sets.keys() if other != vehicle))
                    # Exclusive neighbors for the current vehicle
                    unique_neighbors = neighbor_set - others_union
                    exclusive_neighbors[vehicle] = list(unique_neighbors)
                    successful_transmissions.update(exclusive_neighbors)
                else:
                    pass
    for key, values in successful_transmissions.items():
        if key in values:
            values.remove(key)  # This removes the vehicle from its neighbor list in place
    return  successful_transmissions

##alternative function
# def package_received(attempt_transmission,station_info,attacker_start_index,attackers_info):
#     successful_transmissions = {}
#     for channel, transmitters in attempt_transmission.items():
#         vehicle_transmitters = [t for t in transmitters if t < attacker_start_index]
#         attacker_transmitters = [t for t in transmitters if t >= attacker_start_index]

#         if  len(transmitters) == 1 and len(vehicle_transmitters) == 1:
#             vehicle = vehicle_transmitters[0]
#             successful_transmissions[vehicle] = station_info[vehicle]['neighbors']
#         else:     
#             all_neighbors = {}
#             for vehicle in vehicles:
#                 if vehicle < attacker_start_index:
#                     all_neighbors[vehicle] = station_info[vehicle]['neighbors']
#                 else:
#                     all_neighbors[vehicle] = attackers_info[vehicle]['neighbors']

#             sets = {key: set(value) for key, value in all_neighbors.items()}

#             # Find overlapping part (intersection of all sets)
#             exclusive_neighbors = {}
#             for vehicle, neighbor_set in sets.items():
#                 if vehicle < attacker_start_index:
#                     # Union of neighbors of all other vehicles
#                     others_union = set().union(*(sets[other] for
#                                     other in sets.keys() if other != vehicle))
#                     # Exclusive neighbors for the current vehicle
#                     unique_neighbors = neighbor_set - others_union
#                     exclusive_neighbors[vehicle] = list(unique_neighbors)
#                     successful_transmissions.update(exclusive_neighbors)
#                 else:
#                     pass
#     for key, values in successful_transmissions.items():
#         if key in values:
#             values.remove(key)  # This removes the vehicle from its neighbor list in place
#     return  successful_transmissions

def calculate_PRR(success_num, total_neighbors):
    return Fraction(success_num, total_neighbors)


def IPGModel_Berry(transmissions,IPG_Storage , subframe,vehicles_index):
    for vehicle in vehicles_index:
        neighbors = transmissions[vehicle]
        for neighbor in neighbors:
            IPG_Storage[vehicle][neighbor].append(subframe)



def AOI_last_update(Last_update_Storage,subframe,transmissions,vehicles_index):
    for vehicle in vehicles_index:
        neighbors = transmissions[vehicle]
        for neighbor in neighbors:
            Last_update_Storage[vehicle][neighbor] = subframe



def AOI_model(Last_update_Storage,subframe,AOI_Storage):
    for vehicle, neighbors in Last_update_Storage.items():
        for neighbor, last_update in neighbors.items():
            AOI_Storage[vehicle][neighbor].append(subframe - last_update)



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



def merge_data(ipg_data):
    merged_list = []
    for transmitter, neighbors in ipg_data.items():
        for neighbor, ipg_list in neighbors.items():
            merged_list.extend(ipg_list)  # Add all elements from the IPG list
    return merged_list



def calculate_ipg_tail(data_list):
    # Calculate the CCDF for IPG
    ipg_array = np.array(data_list)
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



def calculate_aoi_tail(data_list):
    # Calculate the CCDF for IPG
    aoi_array = np.array(data_list)
    aoi_0ms_prob = np.sum(aoi_array == 0) / len(aoi_array)

    aoi_sorted = np.sort(aoi_array) * 100  # Convert sub-frames to milliseconds (assuming 1 sub-frame = 100 ms)
    unique_value, counts = np.unique(aoi_sorted, return_counts= True)

    cdf = np.cumsum(counts)/len(aoi_sorted)
    ccdf = 1 - cdf
    target_ccdf = 10 ** -5
    interpolator = interp1d(ccdf, unique_value, fill_value="extrapolate")
    x_value_at_target_ccdf = interpolator(target_ccdf)
    print(f"X-axis value at CCDF = 10^-5 : {x_value_at_target_ccdf}")
    print("Probability of 0ms AOI:", aoi_0ms_prob)
    return unique_value, ccdf,counts



def neighbor_values(vehicles_info,num_vehicles):
    sum_up = 0
    for vehicle, info in vehicles_info.items():
        sum_up = sum_up + len(info['neighbors'])
    print(f"the number of neighbor update is {sum_up - num_vehicles}")



# # Plotting the CCDF of IPG
def plot_ipg_tail(unique_value, ccdf):
    plt.figure(figsize=(15, 8))
    plt.plot(unique_value, ccdf, label='CCDF of IPG')
    plt.xlabel('Inter-Packet Gap (IPG) [ms]')
    plt.ylabel('CCDF')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.title('CCDF of Inter-Packet Gap (IPG)')
    plt.legend()
    plt.grid(True)



def plot_aoi_tail(unique_value, ccdf):
    plt.figure(figsize=(15, 8))
    plt.plot(unique_value, ccdf, label='CCDF of AOI')
    plt.xlabel('Age of information [ms]')
    plt.ylabel('CCDF')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.title('CCDF of Age of Information (AOI)')
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









