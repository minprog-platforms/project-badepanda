from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(10, 165, 100, 33, 33)
speedmax = []
speedbest = []

for dagen in range(100):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    speed = []
    keys = model.schedule._agents.keys()
    for key in keys:
        agent = model.schedule._agents[key]
        if isinstance(agent, MannetjeAgent):
            speed.append(agent.speed)

    model.step_day()
    speedmax.append(max(speed))
    speedbest.append(max(set(speed), key=speed.count))

plt.plot(speedmax)
plt.plot(speedbest)

plt.show()