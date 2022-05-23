from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(10, 363, 100, 33, 33)
speedlist = []

for dagen in range(500):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    speed = []
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        for agent in cell_content:
            if isinstance(agent, MannetjeAgent):
                speed.append(agent.speed)

    model.step_day()
    speedlist.append(max(speed))

plt.plot(speedlist)

plt.show()