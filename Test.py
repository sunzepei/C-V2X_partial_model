

successful_transmissions = {0: [0], 2: [2,4, 5], 1: [0,1, 2, 3, 4], 3: [0, 1, 2,3, 4, 5, 6], 
                            4: [1, 2, 3,4], 7: [8, 9], 5: [2, 3, 4, 6, 7, 8], 6: [3, 4, 5, 7, 8, 9], 8: [5], 9: []} 

def return_successful_transmissions(successful_transmissions):
    for key, values in successful_transmissions.items():
        if key in values:
            values.remove(key)  # This removes the vehicle from its neighbor list in place
    return successful_transmissions

a = return_successful_transmissions(successful_transmissions)
print(a)