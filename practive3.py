import random
import simpy

class Car(object):
    def __init__(self, env, name, bcs, *args, **kwargs):
        self.env = env
        self.name = name
        self.bcs = bcs
        self.last_charge = 0
        self.charge_cap = 10
        self.charge_duration = 5
        self.action = env.process(self.run())

    def run(self):
        while(True):
            print('%s starting to drive' % (self.name))
            trip_duration = self.trip_dur()
            yield self.env.timeout(trip_duration)

            print('%s parking to charge at %d' % (self.name, self.env.now))
            with self.bcs.request() as req:
                yield req
                print('%s starting to charge at %d' % (self.name, self.env.now))

                charge_duration = 5
                try:
                    yield self.env.process(self.charge(charge_duration))
                except simpy.Interrupt:
                    print('Charging of %s was interrupted'%self.name)
                self.update_charge_stats()

    def update_charge_stats(self):
        self.charge_cap = (self.env.now-self.last_charge)*2
        self.last_charge = self.env.now

    def trip_dur(self):
        return self.charge_cap/self.charge_duration

    def charge(self, duration):
        yield self.env.timeout(duration)

def driver(env, car):
    while(True):
        if(random.randint(0, 1)):
            car.action.interrupt()

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(1, 5):
    acar = Car(env, "car%d"%i, bcs)
    env.process(driver(env, acar))

env.run(until=15)
