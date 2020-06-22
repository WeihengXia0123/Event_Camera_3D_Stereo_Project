import simpy
from EventSimulator import EventSimulator
env = simpy.Environment()
sim = EventSimulator(env)
# env.run(until=20)
data = sim.loadData('C:/Users/7zieg/Downloads/BioVision/cam1/events.txt')
print(data.shape)
