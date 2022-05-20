from numpy import isin
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
import random

class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_eaten = 0
class MannetjeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energie = 5
        # self.gen1 = gen1
        # self.gen2 = gen2
        # self.gen3 = gen3
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


    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, FoodAgent) and other.is_eaten == 0:
                other.is_eaten = 1
                self.has_eaten += 1
    
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
        self.num_food = num_food

        for i in range(self.num_agents):
            mannetje = MannetjeAgent(i, self)
            self.schedule.add(mannetje)
            R = random.randint(0,1)
            if R == 1:
                x = self.random.randrange(self.grid.width)
                y = random.choice([0, height - 1])
            elif R == 0:
                x = random.choice([0, width - 1])
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(mannetje, (x, y))
        
        for j in range(1, self.num_food + 1):
            self.num_agents = self.num_agents + j
            food = FoodAgent(self.num_agents, self)
            self.schedule.add(food)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(food, (x, y))

        # self.spawn_food()
    def energie(self):
        energie = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            for agent in cell_content:
                if isinstance(agent, MannetjeAgent):
                    energie += agent.energie
        return energie

    def despawn_food(self):
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            for agent in cell_content:
                if isinstance(agent, FoodAgent):
                    agent.is_eaten = 0
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    self.grid.move_agent(agent, (x,y))

    def new_day(self):
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            for agent in cell_content:
                if isinstance(agent, MannetjeAgent):
                    if agent.has_eaten == 0 and agent not in self.kill_list:
                        self.kill_list.append(agent)
                    elif agent.has_eaten == 1:
                        agent.energie = 5
                        agent.has_eaten = 0
                        R = random.randint(0,1)
                        if R == 1:
                            x = self.random.randrange(self.grid.width)
                            y = random.choice([0, self.grid.height - 1])
                        elif R == 0:
                            x = random.choice([0, self.grid.width - 1])
                            y = self.random.randrange(self.grid.height)
                        self.grid.move_agent(agent, (x,y))
                    # elif agent.has_eaten >= 2:
                    #     agent.energie = 5
                    #     agent.has_eaten = 0
                    #     R = random.randint(0,1) 
                    #     if R == 1:
                    #         x = self.random.randrange(self.grid.width)
                    #         y = random.choice([0, self.grid.height - 1])
                    #     elif R == 0:
                    #         x = random.choice([0, self.grid.width - 1])
                    #         y = self.random.randrange(self.grid.height)
                        # self.grid.move_agent(agent, (x,y))
                        self.num_agents += 1
                        mannentje = MannetjeAgent(self.num_agents, self)
                        self.schedule.add(mannentje)
                        self.grid.place_agent(mannentje, (x,y))

    def kill(self):
        for x in self.kill_list:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_list.remove(x)

    def step(self):
        self.schedule.step()
        return self.energie()

    def step_day(self):
        self.new_day()
        self.kill()
        self.despawn_food()
