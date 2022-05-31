from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image
import pandas as pd
from collections import Counter

model = WorldModel(10, 99, 100, 33, 33 , 1)
for dagen in range(365):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    model.step_day()
    model_data= model.datacollector.get_model_vars_dataframe()

agent_vision = []
agent_speed = []

for agent in model.schedule.agents:
        if isinstance(agent, MannetjeAgent):
            agent_vision.append(agent.vision)
            agent_speed.append(agent.speed)

model_data = model_data.drop('Speed', 1).assign(**model_data.Speed.dropna().apply(pd.Series))
model_data = model_data.drop('Vision', 1).assign(**model_data.Vision.dropna().apply(pd.Series))

model = WorldModel(10, 99, 100, 33, 33, 0)
for dagen in range(365):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    model.step_day()
    model_no_green_beard = model.datacollector.get_model_vars_dataframe()

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(model_data["Totaal"])
axs[0, 0].set_title('Total population')
axs[0, 0].set_ylabel('Total population')
axs[0, 0].set_xlabel('Number of days')
line1, = axs[0, 1].plot(model_data["Altruism"],label='Green Beard')
line2, = axs[0, 1].plot(model_no_green_beard["Altruism"], label='No Green Beard')
axs[0, 1].set_title('Altruism')
axs[0, 1].legend(handles=[line1, line2])
axs[0, 1].set_ylabel('Prevalence')
axs[0, 1].set_xlabel('Number of days')

speed = []
vision = []
for column in model_data:
    if 'Speed' in column:
        axs[1, 0].plot(model_data[column])
        speed.append(column)
    if 'Vision' in column:
        axs[1, 1].plot(model_data[column])
        vision.append(column)

axs[1, 0].legend(speed)
axs[1, 0].set_title('Speed')
axs[1, 1].legend(vision)
axs[1, 0].set_ylabel('Prevalence')
axs[1, 0].set_xlabel('Number of days')
axs[1, 1].set_title('Vision')
axs[1, 1].set_ylabel('Prevalence')
axs[1, 1].set_xlabel('Number of days')

# count the occurrences of each point
c = Counter(zip(agent_speed,agent_vision))
# create a list of the sizes, here multiplied by 10 for scale
s = [10*c[(xx,yy)] for xx,yy in zip(agent_speed,agent_vision)]
plt.figure(2)
plt.scatter(agent_speed, agent_vision, s=s)
plt.title('Speed/Vision tradeoff')
plt.xlabel('Speed')
plt.ylabel('Vision')
plt.show()