from predator_prey import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = ForestModel(300, 100, 100, [90,10],500)

def barlist(n): 
    for i in range(n):
        model.step()
        prey = 0
        predator = 0
        for cell in model.grid.coord_iter():
            cell_content, x, y = cell
            for animal in cell_content:
                if isinstance(animal, PreyAgent):
                    prey += 1
                elif isinstance(animal, PredatorAgent):
                    predator += 1
    return prey, predator

fig=plt.figure()

n=10000 #Number of frames
x=['Prey', 'Predator']
barcollection = plt.bar(x,barlist(1))

def animate(i):
    y=barlist(i+1)
    for i, b in enumerate(barcollection):
        b.set_height(y[i])

anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n,interval=100)

plt.show()