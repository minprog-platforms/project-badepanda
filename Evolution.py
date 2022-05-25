from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
import random
import numpy as np


def compute_altruism(model):
    agent_altruism = [] 
    for agent in model.schedule.agents:
        if isinstance(agent, MannetjeAgent):
            agent_altruism.append(agent.altruism)
    mean = np.mean(agent_altruism)
    return mean

def compute_vision(model):
    agent_vision = [] 
    for agent in model.schedule.agents:
        if isinstance(agent, MannetjeAgent):
            agent_vision.append(agent.vision)
    vision = dict((x,agent_vision.count(x)) for x in set(agent_vision))
    return vision

def compute_speed(model):
    agent_speed = [] 
    for agent in model.schedule.agents:
        if isinstance(agent, MannetjeAgent):
            agent_speed.append(agent.speed)
    speed = dict((x,agent_speed.count(x)) for x in set(agent_speed))
    return speed
def compute_population(model):
    mannetjes = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MannetjeAgent):
            mannetjes += 1
    return mannetjes
class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_eaten = 0

class MannetjeAgent(Agent):
    def __init__(self, unique_id, model, speed, vision, altruism):
        super().__init__(unique_id, model)
        self.energie = self.model.mannetje_energie
        self.has_eaten = 0
        self.speed = speed
        self.altruism = altruism
        self.vision = vision
        self.size = 1
        self.plan = None
        self.green_beard = True

    def move(self):
        cost = (self.speed ** 2) + (self.vision ** 2)
        if self.energie - cost >= 0 and self.energie > 0:
            if self.plan is None:
                neighbors = self.model.grid.get_neighbors(self.pos, radius=self.vision, include_center = False)
                food = []
                for neighbor in neighbors:
                    if isinstance(neighbor, FoodAgent):
                        food.append(neighbor)
                if food:
                    food = self.random.choice(food)
                    self.plan = food
                    position = food.pos

                else:
                    x = self.random.uniform(0, self.model.grid.width)
                    y = self.random.uniform(0, self.model.grid.height)
                    position = (x,y)
            else:
                food = self.plan
                position = food.pos

            distance = self.model.grid.get_distance(self.pos, position)

            if distance <= self.speed:
                self.model.grid.move_agent(self, position)
                self.plan = None
            else:
                heading = self.model.grid.get_heading(self.pos, position)
                new_pos = ((heading/distance) * (self.speed)) + self.pos
                self.model.grid.move_agent(self, new_pos)

            self.energie = self.energie - cost


    def eat(self):
        cellmates = self.model.grid.get_neighbors(self.pos, radius=self.size, include_center = False)
        for other in cellmates:
            if isinstance(other, FoodAgent) and other.is_eaten == 0:
                other.is_eaten = 1
                self.has_eaten += 1
    
    def step(self):
        self.move()
        self.eat()

class WorldModel(Model):

    def __init__(self, mannetjes, num_food, num_energie, width, height):
        self.num_agents = mannetjes
        self.grid = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.kill_list = []
        self.born_list =[]
        self.num_food = num_food
        self.mannetje_energie = num_energie
        self.datacollector = DataCollector(model_reporters={"Altruism": compute_altruism, "Speed": compute_speed , "Vision": compute_vision , "Totaal": compute_population})

        for i in range(self.num_agents):
            altruism = random.randint(0,1)
            mannetje = MannetjeAgent(i, self, 1, 1, altruism)
            self.schedule.add(mannetje)
            R = random.randint(0,1)
            if R == 1:
                x = self.random.uniform(0,self.grid.width)
                y = random.choice([0, height - 1])
            elif R == 0:
                x = random.choice([0, width - 1])
                y = self.random.uniform(0,self.grid.height)
            self.grid.place_agent(mannetje, (x, y))
        
        for j in range(1, self.num_food + 1):
            self.num_agents = self.num_agents + j
            food = FoodAgent(self.num_agents, self)
            self.schedule.add(food)
            x = self.random.uniform(0,self.grid.width)
            y = self.random.uniform(0,self.grid.height)
            self.grid.place_agent(food, (x, y))
        
        
    def energie(self):
        energie = 0
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, MannetjeAgent):
                if agent.energie < 0:
                    energie += 0
                else:
                    energie += agent.energie
        return energie

    def despawn_food(self):
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, FoodAgent):
                agent.is_eaten = 0
                x = self.random.uniform(0,self.grid.width)
                y = self.random.uniform(0,self.grid.height)
                self.grid.move_agent(agent, (x,y))

    def new_day(self):
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, MannetjeAgent):
                if agent.has_eaten == 0 and agent not in self.kill_list:
                    self.kill_list.append(agent)
                elif agent.has_eaten == 1:
                    agent.energie = self.mannetje_energie
                    agent.has_eaten = 0
                    R = random.randint(0,1)
                    if R == 1:
                        x = self.random.uniform(0,self.grid.width)
                        y = random.choice([0, self.grid.height - 1])
                    elif R == 0:
                        x = random.choice([0, self.grid.width - 1])
                        y = self.random.uniform(0,self.grid.height)
                    self.grid.move_agent(agent, (x,y))
                elif agent.has_eaten >= 2:
                    if agent.has_eaten > 2 and agent.altruism == 1:
                        for other in self.kill_list:
                            if other.altruism == 1:
                                self.kill_list.remove(other)
                                break
                    agent.energie = self.mannetje_energie
                    agent.has_eaten = 0
                    R = random.randint(0,1) 
                    if R == 1:
                        x = self.random.uniform(0,self.grid.width)
                        y = random.choice([0, self.grid.height - 1])
                    elif R == 0:
                        x = random.choice([0, self.grid.width - 1])
                        y = self.random.uniform(0,self.grid.height)
                    self.grid.move_agent(agent, (x,y))
                    self.num_agents += 1
                    speed = agent.speed
                    vision = agent.vision
                    if speed == 1:
                        speed = random.randint(1,2)
                    else:
                        speed = random.choices([speed - 1, speed, speed + 1], [1, 1, 1]).pop()

                    if vision == 1:
                        vision = random.randint(1,2)
                    else:
                        vision = random.choices([vision - 1, vision, vision + 1], [1, 1, 1]).pop()
                    
                    mannentje = MannetjeAgent(self.num_agents, self, speed, vision, agent.altruism)
                    self.born_list.append(mannentje)

    def kill(self):
        for x in self.kill_list:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_list.remove(x)

    def born(self):
        for mannetje in self.born_list:
            self.schedule.add(mannetje)
            R = random.randint(0,1) 
            if R == 1:
                x = self.random.uniform(0,self.grid.width)
                y = random.choice([0, self.grid.height - 1])
            elif R == 0:
                x = random.choice([0, self.grid.width - 1])
                y = self.random.uniform(0,self.grid.height)
            self.grid.place_agent(mannetje, (x,y))
            self.born_list.remove(mannetje)
            

    def step(self):
        self.schedule.step()
        return self.energie()

    def step_day(self):
        self.new_day()
        self.kill()
        self.born()
        self.despawn_food()
        self.datacollector.collect(self)
