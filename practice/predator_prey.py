from mesa import Agent, Model
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
import random

from numpy import isin

class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dead_time = 100
    def excist(self):
        self.dead_time = self.dead_time -1

    def dead(self):
        if self.dead_time < 1 and self not in self.model.kill_list:
            self.model.kill_list.append(self)

    def procreate(self):
        P = random.random()
        if P > 0.99 and self.model.num_agents <= self.model.max_num:
            self.model.num_agents += 1
            food = FoodAgent(self.model.num_agents, self.model)
            self.model.schedule.add(food)
            self.model.grid.place_agent(food, self.pos)

    def step(self):
        self.excist()
        self.procreate()
        self.dead()
class PreyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dead_time = 50

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        steps = []
        for step in possible_steps:
            count_food = 0
            count_predator = 0
            cell = self.model.grid.get_cell_list_contents(step)
            for agent in cell:
                if isinstance(agent, FoodAgent):
                    count_food += 1
                elif isinstance(agent, PredatorAgent):
                    count_predator += 1
            if count_food > 0 and count_predator < 1:
                steps.append(step)
        
        if len(steps) < 1:
            steps = possible_steps

        new_position = self.random.choice(steps)
        self.model.grid.move_agent(self, new_position)
        self.dead_time = self.dead_time - 1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, FoodAgent) and other not in self.model.kill_list:
                self.model.kill_list.append(other)
                self.dead_time = 50

    def dead(self):
        if self.dead_time < 1 and self not in self.model.kill_list:
            self.model.kill_list.append(self)

    def procreate(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, PreyAgent):
                P = random.random()
                if P > 0.98 and self.model.num_agents <= self.model.max_num:
                    self.model.num_agents += 1
                    animal = PreyAgent(self.model.num_agents, self.model)
                    self.model.schedule.add(animal)
                    self.model.grid.place_agent(animal, self.pos)
                    self.dead_time = self.dead_time - 1

    def step(self):
        self.move()
        self.eat()
        self.procreate()
        self.dead()

class PredatorAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dead_time = 50

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        steps = []

        for step in possible_steps:
            count = 0
            cell = self.model.grid.get_cell_list_contents(step)
            for animal in cell:
                if isinstance(animal, PreyAgent):
                    count += 1
            if count > 0:
                steps.append(step)

        if len(steps) < 1:
            steps = possible_steps


        new_position = self.random.choice(steps)
        self.model.grid.move_agent(self, new_position)
        self.dead_time = self.dead_time - 1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, PreyAgent) and other not in self.model.kill_list:
                self.model.kill_list.append(other)
                self.dead_time = 25

    def dead(self):
        if self.dead_time < 1 and self not in self.model.kill_list:
            self.model.kill_list.append(self)
    
    def procreate(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, PredatorAgent):
                P = random.random()
                if P > 0.98 and self.model.num_agents <= self.model.max_num:
                    self.model.num_agents += 1
                    animal = PredatorAgent(self.model.num_agents, self.model)
                    self.model.schedule.add(animal)
                    self.model.grid.place_agent(animal, self.pos)
                    self.dead_time = self.dead_time - 1

    def step(self):
        self.move()
        self.eat()
        self.procreate()
        self.dead()

class ForestModel(Model):
    """A model with some number of agents."""

    def __init__(self, animals, width, height, weights, num_food):
        self.num_animals = animals
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByType(self)
        self.kill_list = []
        self.num_food = num_food
        self.num_agents = self.num_animals + self.num_food
        self.max_num = width * height
        animals = ['prey', 'predator']
        # Create agents
        for i in range(self.num_animals):
            animal_type = self.random.choices(animals,weights=weights, k=1).pop()
            if animal_type == 'prey':
                animal = PreyAgent(i, self)
            elif animal_type == 'predator':
                animal = PredatorAgent(i, self)
            
            self.schedule.add(animal)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(animal, (x, y))

        for j in range(self.num_food):
            food_id = self.num_animals + j
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
            self.max_num += 1

    def step(self):
        self.schedule.step_type(PreyAgent)
        self.schedule.step_type(PredatorAgent)
        self.schedule.step_type(FoodAgent)
        self.kill()