from mesa import Agent, Model
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run


class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class PreyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dead_time = 10

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        steps = []
        for step in possible_steps:
            count = 0
            cell = self.model.grid.get_cell_list_contents(step)
            for food in cell:
                if isinstance(food, FoodAgent):
                    count += 1
            if count == 0:
                steps.append(step)
        if not steps:
            steps = possible_steps

        new_position = self.random.choice(steps)
        self.model.grid.move_agent(self, new_position)
        self.dead_time = self.dead_time - 1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if isinstance(other, FoodAgent) and other not in self.model.kill_list:
                self.model.kill_list.append(other)
                self.dead_time = 20

    def dead(self):
        if self.dead_time < 1 and self not in self.model.kill_list:
            self.model.kill_list.append(self)

    def step(self):
        self.move()
        self.eat()
        self.dead()

class PredatorAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dead_time = 10

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        steps = []

        for step in possible_steps:
            count = 0
            cell = self.model.grid.get_cell_list_contents(step)
            for animal in cell:
                if isinstance(animal, PreyAgent):
                    count += 1
            if count >= 0:
                steps.append(step)
        if not steps:
            steps = possible_steps

        new_position = self.random.choice(steps)
        print(new_position)
        self.model.grid.move_agent(self, new_position)
        self.dead_time = self.dead_time - 1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if isinstance(other, PreyAgent) and other not in self.model.kill_list:
                self.model.kill_list.append(other)
                self.dead_time = 20

    def dead(self):
        if self.dead_time < 1 and self not in self.model.kill_list:
            self.model.kill_list.append(self)

    def step(self):
        self.move()
        self.eat()
        self.dead()


class ForestModel(Model):
    """A model with some number of agents."""

    def __init__(self, animals, width, height, weights, num_food):
        self.num_agents = animals
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByType(self)
        self.kill_list = []
        self.num_food = num_food
        animals = ['prey', 'predator']
        # Create agents
        for i in range(self.num_agents):
            animal_type = self.random.choices(animals,weights=weights, k=1).pop()
            if animal_type == 'prey':
                animal = PreyAgent(i, self)
            elif animal_type == 'predator':
                animal = PredatorAgent(i, self)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(animal, (x, y))

        for j in range(self.num_food):
            food = FoodAgent(j, self)
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
        self.schedule.step_type(PreyAgent)
        self.schedule.step_type(PredatorAgent)
        self.kill()