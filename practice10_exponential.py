import simpy
import matplotlib.pyplot as plt
import random
import numpy as np
values = []

def generate_normal(env):
    while(True):
        values.append(random.expovariate(2))
        yield env.timeout(1)

env = simpy.Environment()
env.process(generate_normal(env))

env.run(until=100000)

numpy_values = np.array(values)
plt.hist(
    values,
    100,
    facecolor='red',
    # alpha=0.5,
    label='Mean: %f Stddev:%f'%(numpy_values.mean(), numpy_values.std()))
plt.show()