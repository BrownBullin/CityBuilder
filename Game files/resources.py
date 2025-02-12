class ResourceManager:
    def __init__(self):
        self.resources = {
            'food': 100,
            'wood': 50,
            'stone': 30
        }

    def can_afford(self, cost):
        return all(self.resources.get(resource, 0) >= amount for resource, amount in cost.items())

    def deduct_resources(self, cost):
        for resource, amount in cost.items():
            self.resources[resource] -= amount

    def update(self, city):
        self.resources['food'] -= city.population
        if self.resources['food'] < 0:
            city.happiness -= 10  # Unhappy population if no food
        for row in city.grid:
            for building in row:
                if building:
                    for resource, amount in building.resource_output.items():
                        self.resources[resource] += amount
