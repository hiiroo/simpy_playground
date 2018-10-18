import math
import simpy

aci_second = 6
aci_minute = 6/60
aci_hour = 1/120

second = 0
minute = 0
hour = 0

coincidence = []

def clock_coincidence(env, threshold):
    global second, minute, hour, aci_second, aci_minute, aci_hour
    second=second+1
    minute+=aci_minute
    hour+=aci_hour

    #threshold 0.025
    if(math.fabs(minute-hour) <= threshold):
        coincidence.append(second)

    yield env.timeout(1)

env = simpy.Environment()
env.process(clock_coincidence(env, 0.025))
env.run(until=7200)

print(coincidence)