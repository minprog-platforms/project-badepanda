from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image
model = WorldModel(10, 99, 100, 33, 33)
mannetjes = []
def barlist(n): 
    for dagen in range(n):
        for i in range(10):
            energie = model.step()
            if energie == 0:
                break
        food = 0
        mannetje = 0
        keys = model.schedule._agents.keys()
        for key in keys:
            agent = model.schedule._agents[key]
            if isinstance(agent, MannetjeAgent):
                mannetje += 1
            elif isinstance(agent, FoodAgent):
                food += 1
        model.step_day()
    print(mannetje)
    mannetjes.append(mannetje)
    return mannetje, food
fig=plt.figure()

n=100 #Number of frames
x=['Mannetjes', 'Food']
barcollection = plt.bar(x,barlist(1))

def animate(i):
    y=barlist(i+1)
    for i in range(len(barcollection)):
        barcollection[i].set_height(y[i])

anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n,interval=100)

plt.show()