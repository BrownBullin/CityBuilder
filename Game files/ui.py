import pygame
from building import Building

class UIManager:
    def __init__(self, screen, city, resource_manager):
        self.screen = screen
        self.city = city
        self.resource_manager = resource_manager
        self.font = pygame.font.Font(None, 36)
        self.sidebar_width = 200
        self.selected_building = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < self.city.grid_size[0] * 64:
                self.handle_grid_click(x, y)
            else:
                self.handle_sidebar_click(y)

    def handle_grid_click(self, x, y):
        grid_x, grid_y = x // 64, y // 64
        if self.selected_building:
            building = Building(self.selected_building["name"], **self.selected_building)
            self.city.place_building(building, grid_x, grid_y, self.resource_manager)

    def handle_sidebar_click(self, y):
        if 50 <= y <= 100:
            self.selected_building = {"name": "Farm", "cost": {"wood": 10}, "resource_output": {"food": 5}}
        elif 120 <= y <= 170:
            self.selected_building = {"name": "House", "cost": {"wood": 15}, "resource_output": {}}

    def render(self):
        self.render_grid()
        self.render_sidebar()

    def render_grid(self):
        for x in range(self.city.grid_size[0]):
            for y in range(self.city.grid_size[1]):
                rect = pygame.Rect(x * 64, y * 64, 64, 64)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def render_sidebar(self):
        pygame.draw.rect(self.screen, (240, 240, 240), (self.city.grid_size[0] * 64, 0, self.sidebar_width, 768))
        y = 10
        for resource, amount in self.resource_manager.resources.items():
            text = self.font.render(f"{resource.capitalize()}: {amount}", True, (0, 0, 0))
            self.screen.blit(text, (self.city.grid_size[0] * 64 + 10, y))
            y += 40
