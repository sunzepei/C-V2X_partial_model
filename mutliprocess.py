import numpy as np

resource_map = np.random.randint(0, 2, (10, 10))
print(resource_map)
subchannel_usage = np.sum(resource_map[0:3, :] > 0, axis=1)
print(subchannel_usage)