from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
import random
import numpy as np


# Make the world for the tiny people to life in
class WorldModel(Model):
    # Initialize the world with the number of people, food and energy for the people
    # The width and height of the world can be chosen aswell as if the people have green beards if they are altuistic
    def __init__(self, num_people, num_food, num_energy, width, height, green_beard):
        self.num_agents = num_people
        self.grid = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.kill_list = []
        self.born_list = []
        self.num_food = num_food
        self.Tiny_man_energy = num_energy
        self.green_beard = green_beard
        self.datacollector = DataCollector(
            model_reporters={"Totaal": compute_population, "Altruism": compute_altruism,
                             "Speed": compute_speed, "Vision": compute_vision})

        # A loop to put all the tiny agents in world
        for i in range(self.num_agents):

            # Half of the agents is altruistic
            if i < 0.5*self.num_agents:
                altruism = 0
            else:
                altruism = 1
            # Make the tiny agent
            Tiny_man = Tiny_manAgent(i, self, 1, 1, altruism)
            # Put them in the schedule
            self.schedule.add(Tiny_man)
            # Put the tiny man agent on te egde on the map
            R = random.randint(0, 1)
            if R == 1:
                x = self.random.uniform(0, self.grid.width)
                y = random.choice([0, height - 1])
            elif R == 0:
                x = random.choice([0, width - 1])
                y = self.random.uniform(0, self.grid.height)
            self.grid.place_agent(Tiny_man, (x, y))
        # A loop to put all the food in the world
        for j in range(1, self.num_food + 1):
            self.num_agents = self.num_agents + j
            food = FoodAgent(self.num_agents, self)
            self.schedule.add(food)
            x = self.random.uniform(0, self.grid.width)
            y = self.random.uniform(0, self.grid.height)
            self.grid.place_agent(food, (x, y))

    # Calculate how much energy there is left in all the tiny man
    def energy(self):
        energy = 0
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, Tiny_manAgent):
                if agent.energy < 0:
                    energy += 0
                else:
                    energy += agent.energy
        return energy

    # Relocate all the food for the new day
    def despawn_food(self):
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, FoodAgent):
                agent.is_eaten = 0
                x = self.random.uniform(0, self.grid.width)
                y = self.random.uniform(0, self.grid.height)
                self.grid.move_agent(agent, (x, y))

    # After a long day all the tiny man go home and new little man get born but with genetic mutations
    def new_day(self):
        keys = self.schedule._agents.keys()
        for key in keys:
            agent = self.schedule._agents[key]
            if isinstance(agent, Tiny_manAgent):

                # If tiny agent has not eaten they die
                if agent.has_eaten == 0 and agent not in self.kill_list:
                    self.kill_list.append(agent)

                # If tiny agent has eaten one food they survive but do not procreate.
                elif agent.has_eaten == 1:
                    # Reset the agents
                    agent.energy = self.Tiny_man_energy
                    agent.has_eaten = 0
                    R = random.randint(0, 1)
                    if R == 1:
                        x = self.random.uniform(0, self.grid.width)
                        y = random.choice([0, self.grid.height - 1])
                    elif R == 0:
                        x = random.choice([0, self.grid.width - 1])
                        y = self.random.uniform(0, self.grid.height)
                    self.grid.move_agent(agent, (x, y))

                # If agent has eaten 2 or more food they survive and can procreate
                elif agent.has_eaten >= 2:

                    # If agent is altruistic they can save an other agents life
                    if agent.has_eaten > 2 and agent.altruism == 1:
                        for other in self.kill_list:
                            # If green_beard is 1 means that the agent can see if other agents are also altruistic
                            if self.green_beard == 1:
                                if other.altruism == 1:
                                    self.kill_list.remove(other)
                                    break
                            elif self.green_beard == 0:
                                self.kill_list.remove(other)
                                break
                    # Reset the agents
                    agent.energy = self.Tiny_man_energy
                    agent.has_eaten = 0
                    R = random.randint(0, 1)
                    if R == 1:
                        x = self.random.uniform(0, self.grid.width)
                        y = random.choice([0, self.grid.height - 1])
                    elif R == 0:
                        x = random.choice([0, self.grid.width - 1])
                        y = self.random.uniform(0, self.grid.height)
                    self.grid.move_agent(agent, (x, y))
                    self.num_agents += 1

                    # The mutations for speed and vision happen here
                    speed = agent.speed
                    vision = agent.vision
                    if speed == 1:
                        speed = random.randint(1, 2)
                    else:
                        speed = random.choices([speed - 1, speed, speed + 1], [1, 1, 1]).pop()

                    if vision == 1:
                        vision = random.randint(1, 2)
                    else:
                        vision = random.choices([vision - 1, vision, vision + 1], [1, 1, 1]).pop()

                    mannentje = Tiny_manAgent(self.num_agents, self, speed, vision, agent.altruism)
                    self.born_list.append(mannentje)

    # Remove agents from the simulation
    def kill(self):
        for x in self.kill_list:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_list.remove(x)

    # Add agents to the simulation
    def born(self):
        for Tiny_man in self.born_list:
            self.schedule.add(Tiny_man)
            R = random.randint(0, 1)
            if R == 1:
                x = self.random.uniform(0, self.grid.width)
                y = random.choice([0, self.grid.height - 1])
            elif R == 0:
                x = random.choice([0, self.grid.width - 1])
                y = self.random.uniform(0, self.grid.height)
            self.grid.place_agent(Tiny_man, (x, y))
            self.born_list.remove(Tiny_man)

    # Let the tiny man move through the world
    def step(self):
        self.schedule.step()
        return self.energy()

    # If all the tiny man have no more energy they go home and a data is collected
    # A new day is started food respawns tiny man are killed and born
    def step_day(self):
        self.datacollector.collect(self)
        self.new_day()
        self.kill()
        self.born()
        self.despawn_food()


# Make the food for the tiny people to eat
class FoodAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_eaten = 0


# Make the Tiny agents
class Tiny_manAgent(Agent):

    # When tiny man are born they have a speed, vision and altruism trait
    def __init__(self, unique_id, model, speed, vision, altruism):
        super().__init__(unique_id, model)
        self.energy = self.model.Tiny_man_energy
        self.has_eaten = 0
        self.speed = speed
        self.altruism = altruism
        self.vision = vision
        self.size = 1
        self.plan = None
        self.green_beard = True

    # Let the tiny man move through the world
    def move(self):
        # It costs more energy if you are faster or have better vision
        cost = (self.speed ** 2) + (self.vision * 2)
        if self.energy - cost >= 0 and self.energy > 0:

            # If the tiny man has already seen food the next step it remembers that and do not need to search again
            if self.plan is None:
                neighbors = self.model.grid.get_neighbors(self.pos, radius=self.vision, include_center=False)
                food = []
                for neighbor in neighbors:
                    if isinstance(neighbor, FoodAgent):
                        food.append(neighbor)
                if food:
                    food = self.random.choice(food)
                    self.plan = food
                    position = food.pos

                # If no food is found move random
                else:
                    x = self.random.uniform(0, self.model.grid.width)
                    y = self.random.uniform(0, self.model.grid.height)
                    position = (x, y)
            else:
                food = self.plan
                position = food.pos

            distance = self.model.grid.get_distance(self.pos, position)

            # If speed is sufficient go to te food otherwise move in de direction
            if distance <= self.speed:
                self.model.grid.move_agent(self, position)
                self.plan = None
            else:
                heading = self.model.grid.get_heading(self.pos, position)
                new_pos = ((heading/distance) * (self.speed)) + self.pos
                self.model.grid.move_agent(self, new_pos)

            self.energy = self.energy - cost

    # If food is found eat the food
    def eat(self):
        cellmates = self.model.grid.get_neighbors(self.pos, radius=self.size, include_center=False)
        for other in cellmates:
            if isinstance(other, FoodAgent) and other.is_eaten == 0:
                other.is_eaten = 1
                self.has_eaten += 1

    def step(self):
        self.move()
        self.eat()


# Compute the mean altruism of the population
def compute_altruism(model):
    agent_altruism = []
    for agent in model.schedule.agents:
        if isinstance(agent, Tiny_manAgent):
            agent_altruism.append(agent.altruism)
    mean = np.mean(agent_altruism)
    return mean


# Count how many tiny man there are for the different vision levels
def compute_vision(model):
    agent_vision = []
    for agent in model.schedule.agents:
        if isinstance(agent, Tiny_manAgent):
            agent_vision.append(agent.vision)
    vision = dict(("Vision {}".format(x), agent_vision.count(x)) for x in set(agent_vision))
    return vision


# Count how many tiny man there are for the different speed levels
def compute_speed(model):
    agent_speed = []
    for agent in model.schedule.agents:
        if isinstance(agent, Tiny_manAgent):
            agent_speed.append(agent.speed)
    speed = dict(("Speed {}".format(x), agent_speed.count(x)) for x in set(agent_speed))
    return speed


# Count the total population size
def compute_population(model):
    Tiny_man = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Tiny_manAgent):
            Tiny_man += 1
    return Tiny_man
