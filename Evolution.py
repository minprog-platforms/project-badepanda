from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
import random

class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class MannetjeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energie = 5
        # self.gen1 = gen1
        # self.gen2 = gen2
        # self.gen3 = gen3
        self.has_eaten = 0

    def move_step(self):
        if self.energie > 0:

            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            steps = []

            for step in possible_steps:
                count = 0
                cell = self.model.grid.get_cell_list_contents(step)
                for animal in cell:
                    if isinstance(animal, FoodAgent):
                        count += 1
                if count > 0:
                    steps.append(step)

            if len(steps) < 1:
                steps = possible_steps

            new_position = self.random.choice(steps)
            self.model.grid.move_agent(self, new_position)
            self.energie = self.energie - 1


    def eat_(self):
        if self.energie > 0 and self not in self.model.kill_list:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for other in cellmates:
                if isinstance(other, FoodAgent) and other not in self.model.kill_list:
                    self.model.kill_list.append(other)
                    self.has_eaten += 1

    def dead(self):
        if self not in self.model.kill_list and self.has_eaten == 0:
            print('hoi')
            self.model.kill_list.append(self)

    def new_day(self):
        if self not in self.model.kill_list:
            self.energie = 5
            self.has_eaten = 0
    
    def procreate(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, MannetjeAgent) and other not in self.model.kill_list:
                P = random.random()
                if P > 0.5:
                    self.model.num_agents += 1
                    mannentje = MannetjeAgent(self.model.num_agents, self.model)
                    self.model.schedule.add(mannentje)
                    self.model.grid.place_agent(mannentje, self.pos)

    def step(self):
        self.move()

    def advance(self):
        self.eat()
class WorldModel(Model):

    def __init__(self, mannetjes, num_food, width, height):
        self.num_agents = mannetjes
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.kill_list = []
        self.procreate_list = []
        self.num_food = num_food
        self.steps = 5

        for i in range(self.num_agents):
            mannetje = MannetjeAgent(i, self)
            self.schedule.add(mannetje)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(mannetje, (x, y))

    def despawn_food(self):
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            for agent in cell_content:
                if isinstance(agent, FoodAgent) and agent not in self.kill_list:
                    self.kill_list.append(agent)

    def spawn_food(self):
        for j in range(1, self.num_food + 1):
            self.num_agents = self.num_agents + j
            food = FoodAgent(self.num_agents, self)
            self.schedule.add(food)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(food, (x, y))

    def kill(self):
        for x in self.kill_list:
            # print(x.unique_id, x)
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_list.remove(x)

    def step(self):
        self.schedule.step_type(MannetjeAgent)

    def step_day(self):
        self.spawn_food()
        self.despawn_food()
        self.kill()
