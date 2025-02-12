class Building:
    def __init__(self, name, cost, resource_output):
        self.name = name
        self.cost = cost
        self.resource_output = resource_output

    def on_place(self, city):
        if self.name == "Park":
            city.happiness += 10
        elif self.name == "Factory":
            city.happiness -= 5
