from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(5, 10, 10, 10)

fig, ax = plt.subplots()
colors_list = ['1', 'orange', 'green']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)
ims = []
for dagen in range(100):
    for i in range(10):
        energie = model.step()
        if energie == 0:
            break
        image = np.zeros((model.grid.width, model.grid.height))
        for cell in model.grid.coord_iter():
            cell_content, x, y = cell
            if len(cell_content) == 1:
                for agent in cell_content:
                    if isinstance(agent, MannetjeAgent):
                        image[x][y] = 1
                    elif isinstance(agent, FoodAgent):
                        image[x][y] = 2

        # # if i == 1:
        # #     ax.imshow(image, cmap=cmap, norm=norm)
        # else:
        im = ax.imshow(image, cmap=cmap, norm=norm, animated=True)
        ims.append([im])
    model.step_day()

ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

plt.show()