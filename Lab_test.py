def generate_attacker_positions(num_vehicles, step):
    """
    Generate attacker positions where each attacker spans a range around a multiple of `step`.

    Args:
        num_vehicles (int): Total number of vehicles.
        step (int): The interval at which attackers are inserted.

    Returns:
        list: List of attacker positions as (left_vehicle, right_vehicle).
    """
    positions = []
    for i in range(step, num_vehicles, step):  # Stop before `num_vehicles`
        left_vehicle = i - 1  # Define the left vehicle
        right_vehicle = i     # Define the right vehicle
        positions.append((left_vehicle, right_vehicle))
    return positions

position = generate_attacker_positions(70, 2)
print(len(position)) 