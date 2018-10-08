import random
import simpy

class Car(object):
    def __init__(self, env, name, *args, **kwargs):
        self.env = env
        self.name = name
        self.action = env.process(self.run())

    def run(self):
        while(True):
            print('%s start parking at %d' % (self.name, self.env.now))
            charge_duration = 5
            try:
                with bcs.request() as req:
                    yield req
                    try:
                        print('%s start charging at %d'%(self.name, self.env.now))
                        yield self.env.process(self.charge(charge_duration))
                    except simpy.Interrupt:
                        print('%s charging was interrupted at %d'%(self.name, self.env.now))

            except simpy.Interrupt:
                print('%s left the charge queue at %d'%(self.name, self.env.now))

            print('%s start driving at %d' % (self.name, self.env.now))
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

def driver(env, car):
    yield env.timeout(3)
    if(random.randint(0, 1)):
        car.action.interrupt()


env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(1, 5):
    car = Car(env, 'Car %d'%i)
    env.process(driver(env, car))

env.run(until=20)
