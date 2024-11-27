successful_transmissions = {
    5: [2, 3, 4],  # Vehicle 5 successfully transmitted to vehicles 2, 3, and 4
    8: [6, 7,3,11],     # Vehicle 8 successfully transmitted to vehicles 6 and 7
    12: [11,2,3,4]       # Vehicle 12 successfully transmitted to vehicle 11
}

inter_mediate = {key: set(value) for key, value in successful_transmissions.items()}

others_union = set().union(*(inter_mediate[other] for
                                 other in inter_mediate.keys()))
print(others_union)