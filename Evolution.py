from mesa import Agent, Model
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
import random

class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class MannetjeAgent(Agent):
    def __init__(self, unique_id, model, gen1, gen2, gen3):
        super().__init__(unique_id, model)
        self.energie = 50
        self.gen1 = gen1
        self.gen2 = gen2
        self.gen3 = gen3
        self.has_eaten = 0

    def move(self):
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
            self.has_eaten += 1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, FoodAgent) and other not in self.model.kill_list:
                self.model.kill_list.append(other)

    def dead(self):
        if self.energie < 1 and self not in self.model.kill_list and self.has_eaten == 0:
            self.model.kill_list.append(self)
    
    def procreate(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, MannetjeAgent):
                P = random.random()
                if P > 0.989 and self.model.num_agents <= self.model.max_num:
                    self.model.num_agents += 1
                    mannentje = MannetjeAgent(self.model.num_agents, self.model)
                    self.model.schedule.add(mannentje)
                    self.model.grid.place_agent(mannentje, self.pos)
                    self.dead_time = self.dead_time - 1

    def step(self):
        self.move()
        self.eat()
        self.procreate()
        self.dead()

class WorldModel(Model):

    def __init__(self, mannetjes, num_food, width, height):
        self.num_mannetjes = mannetjes
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByType(self)
        self.kill_list = []
        self.procreate_list = []
        self.num_food = num_food

        for i in range(self.num_mannetjes):
            mannetje = MannetjeAgent(i, self)
            self.schedule.add(mannetje)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(mannetje, (x, y))

    def made_food(self):
        for j in range(self.num_food):
            food_id = self.num_mannetjes + j
            food = FoodAgent(food_id, self)
            self.schedule.add(food)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(food, (x, y))

    def kill(self):
        for x in self.kill_list:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_list.remove(x)

    def step(self):
        self.schedule.step_type(MannetjeAgent)
        self.schedule.step_type(FoodAgent)
        self.kill()