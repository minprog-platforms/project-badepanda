from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(50, 165, 100, 33, 33)

fig, ax = plt.subplots()
colors_list = ['orange', 'green']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2]
norm = colors.BoundaryNorm(bounds, cmap.N)
ims = []
for j in range(10):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
        x_list= []
        y_list = []
        color_list = []
        keys = model.schedule._agents.keys()
        for key in keys:
            agent = model.schedule._agents[key]
            x, y = agent.pos
            if isinstance(agent, MannetjeAgent):
                x_list.append(x)
                y_list.append(y)
                color_list.append(0)
            elif isinstance(agent, FoodAgent):
                if agent.is_eaten == 0:
                    x_list.append(x)
                    y_list.append(y)
                    color_list.append(1)
        im = ax.scatter(x_list, y_list, c=color_list, cmap=cmap, norm=norm, animated=True)
        ims.append([im])
    model.step_day()

ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

plt.show()