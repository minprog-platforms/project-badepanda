from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(10, 363, 100, 33, 33)
totaallist = []
speed0list = []
speed1list = []
speed2list = []
speed3list = []
speed4list = []
speed5list = []
speed6list = []
speed7list = []
speed8list = []
speed9list = []

for dagen in range(100):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    mannetje = 0
    speed0 = 0
    speed1 = 0
    speed2 = 0
    speed3 = 0
    speed4 = 0
    speed5 = 0
    speed6 = 0
    speed7 = 0
    speed8 = 0
    speed9 = 0
    keys = model.schedule._agents.keys()
    for key in keys:
        agent = model.schedule._agents[key]
        if isinstance(agent, MannetjeAgent):
            mannetje += 1
            if agent.speed == 0:
                speed0 += 1
            elif agent.speed == 1:
                speed1 += 1
            elif agent.speed == 2:
                speed2 += 1
            elif agent.speed == 3:
                speed3 += 1
            elif agent.speed == 4:
                speed4 += 1
            elif agent.speed == 5:
                speed5 += 1
            elif agent.speed == 6:
                speed6 += 1
            elif agent.speed == 7:
                speed7 += 1
            elif agent.speed == 8:
                speed8 += 1
            elif agent.speed == 9:
                speed9 += 1
    model.step_day()
    totaallist.append(mannetje)
    speed0list.append(speed0)
    speed1list.append(speed1)
    speed2list.append(speed2)
    speed3list.append(speed3)
    speed4list.append(speed4)
    speed5list.append(speed5)
    speed6list.append(speed6)
    speed7list.append(speed7)
    speed8list.append(speed8)
    speed9list.append(speed9)

plt.plot(totaallist, 'ko', label='totaal')
plt.plot(speed0list, 'ro', label='speed0')
plt.plot(speed1list, 'go', label='speed1')
plt.plot(speed2list, 'bo', label='speed2')
plt.plot(speed3list, 'co', label='speed3')
plt.plot(speed4list, 'mo', label='speed4')
plt.plot(speed5list, 'yo', label='speed5')
plt.plot(speed6list, color= 'orange', label='speed6')
plt.plot(speed7list, color= 'pink', label='speed7')
# plt.plot(speed8list, color='olive', label='speed8')
# plt.plot(speed9list, color='brown', label='speed9')

plt.legend()
plt.show()