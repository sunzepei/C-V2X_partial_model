# import numpy as np
# import matplotlib.pyplot as plt
# from tqdm import tqdm
# import function as f
# import pandas as pd
# import random

# # Set seed for reproducibility
# seed = 42
# random.seed(seed)  # Seed the built-in random module
# np.random.seed(seed)  # Seed the NumPy random module


# sliding_window_size = 10
# communication_range = 10 # Number of vehicles ahead and behind within communication range
# sps_interval_range = (5,16)
# num_subchannels = 100

# class Vehicle:
#     def __init_(self, number):
#         self.number = number
#         self.communication_range = communication_range
#         self.sps_interval_range = sps_interval_range
#         self.sliding_window_size = sliding_window_size
#         self.neighbors = self.get_neighbors()
#         self.current_subchannel = np.random.choice(num_subchannels)
#         self.next_selection_frame = 0
#         self.sps_counter = np.random.randint(sps_interval_range[0], sps_interval_range[1])
#         self.resource_map = np.zeros((num_subchannels, sliding_window_size), dtype=np.uint8)
#         self.last_update = 0

    
import numpy as np

class BankAccount:
    def __init__(self,Holder_name):
        self.balance = 0
        self.Holder_name = Holder_name
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
    
    def get_balance(self):
        return self.balance

    def future(self):
        return self.get_balance() + 200

accoutn_sun = BankAccount("Sun")
accoutn_sun.deposit(100)
balance_sun = accoutn_sun.get_balance()
future_amount_sun = accoutn_sun.future()
print(future_amount_sun)
print(balance_sun)



