from functools import partial, wraps
import simpy

def trace(env, callback):

    def get_wrapper(env_step, callback):
        @wraps(env_step)
        def tracing_step():
            if (len(env._queue)):
                t, prio, eid, event = env._queue[0]
                callback(t, prio, eid, event)
            return env_step()
        return tracing_step

    env.step = get_wrapper(env.step, callback)

def monitor(data, t, prio, eid, event):
    data.append((('time', t), ('eventId', eid), ('eventType', type(event))))

def test_process(env):
    yield env.timeout(1)

data = []

monitor = partial(monitor, data)

env = simpy.Environment()
trace(env, monitor)

p = env.process(test_process(env))
env.run(until=p)

for d in data:
    print(d)
