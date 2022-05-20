from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image
model = WorldModel(5, 5, 10, 10)

for dagen in range(100):
    for i in range(10):
        energie = model.step()
        if energie == 0:
            break
    food = 0
    mannetje = 0
    image = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        for agent in cell_content:
            if isinstance(agent, MannetjeAgent):
                mannetje += 1
            elif isinstance(agent, FoodAgent):
                    food += 1
    print(mannetje, food)
    model.step_day()
