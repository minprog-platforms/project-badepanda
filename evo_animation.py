from evolution import WorldModel, FoodAgent, Tiny_manAgent
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

# Make the world
model = WorldModel(10, 250, 250, 100, 100, 1)
# Loop for a x amount of days
for dagen in range(1):
    # Let the model step 1000 is arbitrary this stops when the man are out of energy
    for i in range(1000):
        energy = model.step()
        if energy == 0:
            break
    model.step_day()

# Prepare for making beautiful animation
fig, ax = plt.subplots()
colors_list = ['green', 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0, 1, 2]
norm = colors.BoundaryNorm(bounds, cmap.N)
ims = []

# Loop one more day and make a animation
for i in range(1000):
    energy = model.step()
    if energy == 0:
        break
    x_list = []
    y_list = []
    color_list = []
    keys = model.schedule._agents.keys()
    # Loop over all the agents and get there position and type
    for key in keys:
        agent = model.schedule._agents[key]
        x, y = agent.pos
        if isinstance(agent, Tiny_manAgent):
            x_list.append(x)
            y_list.append(y)
            color_list.append(agent.speed)
        elif isinstance(agent, FoodAgent):
            if agent.is_eaten == 0:
                x_list.append(x)
                y_list.append(y)
                color_list.append(0)
    # Make one picture
    im = ax.scatter(x_list, y_list, c=color_list, cmap=cmap, norm=norm, animated=True)
    ims.append([im])

# Make animation and save it
ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
writergif = animation.PillowWriter(fps=30)
ani.save("Animation10days.gif", writer=writergif)
