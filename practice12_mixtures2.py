import simpy
import matplotlib.pyplot as plt
import random
import numpy as np
values = []
    
def generate_mixture(env):
    while(True):
        if(random.random() <= 0.3):
            values.append(random.uniform(0, 4))
        else:
            values.append(random.normalvariate(4, 4))
        yield env.timeout(1)

env = simpy.Environment()
env.process(generate_mixture(env))

env.run(until=100000)

numpy_values = np.array(values)
plt.hist(
    values, 
    100, 
    facecolor='red', 
    # alpha=0.5, 
    label='Mean: %f Stddev:%f'%(numpy_values.mean(), numpy_values.std()))
plt.show()