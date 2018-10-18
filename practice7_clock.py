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
    while(True):
        global second, minute, hour, aci_second, aci_minute, aci_hour
        second+=1
        minute+=aci_minute
        hour+=aci_hour

        # print(math.fabs(minute%360-hour%360))
        if(math.fabs(minute%360-hour%360) <= threshold):
            coincidence.append(second)

        yield env.timeout(1)

env = simpy.Environment()
env.process(clock_coincidence(env, 0.025))
env.run(until=7200)

print([(c/60)%60 for c in coincidence])