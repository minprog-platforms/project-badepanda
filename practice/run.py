from predator_prey import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = ForestModel(300, 100, 100, [90,10],500)
for i in range(100):
    model.step()
    prey = 0
    predator = 0
    food = 0
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        for animal in cell_content:
            if isinstance(animal, PreyAgent):
                prey += 1
            elif isinstance(animal, PredatorAgent):
                predator += 1
            elif isinstance(animal,FoodAgent):
                food += 1
    # print(prey, predator, food)