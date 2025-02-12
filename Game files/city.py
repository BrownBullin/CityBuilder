class City:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        self.population = 10
        self.happiness = 100

    def place_building(self, building, x, y, resource_manager):
        if self.is_within_bounds(x, y) and self.grid[x][y] is None and resource_manager.can_afford(building.cost):
            self.grid[x][y] = building
            building.on_place(self)
            resource_manager.deduct_resources(building.cost)
            return True
        return False

    def is_within_bounds(self, x, y):
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]

    def update(self):
        if self.happiness > 50:
            self.population += 1
        self.population = max(self.population, 1)
