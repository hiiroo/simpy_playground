import random
import math
import simpy
import matplotlib.pyplot as plt

crossings = []
estimations = []

def update_plot(env):
    plt.plot(env.now, estimations[-1], '.')
    yield env.timeout(1)

def estimate_pi(env, n, l, t):
    estimations.append(
        (sum(estimations) +
         (2*n*l)/(t*crossings[-1]))/(len(estimations)+1))
    update_plot(env)
    yield env.process(update_plot(env))

def throw_needles(env, n, l, t):
    while(True):
        yield env.timeout(1)
        thetas = [random.uniform(0, 90) for i in range(n)]
        dists = [random.uniform(0, 1) for i in range(n)]
        thetasp = [theta*math.acos(-1)/180 for theta in thetas]
        _crossings = [1 if dist <= (l/2)*math.sin(thetap) else 0
                      for dist, thetap in zip(dists, thetasp)]
        count = _crossings.count(1)
        crossings.append(count)
        yield env.process(estimate_pi(env, n, l, t))

env = simpy.Environment()
env.process(throw_needles(env, 1000, 2, 2))

env.run(1000)
plt.show()
