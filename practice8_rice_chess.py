import simpy

total = 0 

def compute(env, c):
    global total
    while(True):
        total+=c**env.now
        yield env.timeout(1)

env = simpy.Environment()
env.process(compute(env, 2))

env.run(until=64)#8x8 chessboard

print('Total number of wheat: %d'%total)
