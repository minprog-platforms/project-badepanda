import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import random
class Cell:
    def __init__(self,status, x, y):
        self._status = status
        self._fire_time = 0
        self._coorx = x
        self._coory = y

class Grid:
    def __init__(self, rows ,cols, weights):
        self._max_x = rows - 1
        self._max_y = cols - 1
        self._grid = []
        status_list = ['empty', 'tree', 'cooltree']
        for i in range(rows):
            row = []
            for j in range(cols):
                status = random.choices(status_list, weights).pop()
                cell = Cell(status, i, j)
                row.append(cell)
            self._grid.append(row)

    def step(self):
        image = []
        for row in self._grid:
            image_row = []
            for cell in row:
                if cell._status == 'tree':
                    image_row.append(1)
                elif cell._status == 'cooltree':
                    image_row.append(2)
                elif cell._status == 'fire':
                    image_row.append(3)
                else:
                    image_row.append(0)
            image.append(image_row)

        return image

    def find(self, x, y):
        return self._grid[x][y]

    def chance_fire(self, x, y):
        neighbors = 0
        fire = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                corx = x + i
                cory = y + j
                if 0 <= corx <= self._max_x and 0 <= cory <= self._max_y:
                    neighbors += 1
                    cell = grid.find(corx, cory)
                    if cell._status == 'fire' and cell._fire_time > 1:
                        fire += 1

        return fire/neighbors

    def fire(self):
        for row in self._grid:
            for cell in row:
                if cell._status == 'tree':
                    P = self.chance_fire(cell._coorx, cell._coory)
                    rand = random.uniform(0,0.7)
                    if P > rand:
                        cell._status = 'fire'
                        cell._fire_time = 1
                if cell._status == 'cooltree':
                    P = self.chance_fire(cell._coorx, cell._coory)
                    rand = random.uniform(0,1) + 0.1
                    if P > rand:
                        cell._status = 'fire'
                        cell._fire_time = 1
    def fire_burns(self):
        for row in self._grid:
            for cell in row:
                if cell._status == 'fire' and cell._fire_time <= 5:
                    cell._fire_time += 1
                if cell._status == 'fire' and cell._fire_time > 5:
                    cell._status = 'empty'

    def start_fire(self):
        randx = random.randint(0, self._max_x)
        randy = random.randint(0, self._max_y)
        cell = self.find(randx, randy)
        cell._status = 'fire'


if __name__ == "__main__":
    grid = Grid(33,33,[30,60,10])

    fig, ax = plt.subplots()
    colors_list = ['black', 'green', 'yellow', 'red']
    cmap = colors.ListedColormap(colors_list)
    bounds = [0,1,2,3,4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    image = grid.step()
    ax.imshow(image, cmap=cmap, norm=norm)
    ims = []
    grid.start_fire()
    for i in range(100):
        grid.fire()
        grid.fire_burns()
        image = grid.step()
        im = ax.imshow(image, cmap=cmap, norm=norm, animated=True)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=100)

    plt.show()

