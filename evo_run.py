from evolution import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors, image

model = WorldModel(10, 99, 100, 33, 33)
totaallist = []
for dagen in range(100):
    for i in range(1000):
        energie = model.step()
        if energie == 0:
            break
    model.step_day()
    model_data= model.datacollector.get_model_vars_dataframe()

print(model_data)
model_data["Altruism"].plot.line()
# model_data["Speed"].plot.line()
# model_data["Vision"].plot.line()
model_data["Totaal"].plot.line()
plt.show()