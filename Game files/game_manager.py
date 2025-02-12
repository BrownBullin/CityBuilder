import pygame
from city import City
from resources import ResourceManager
from events import EventManager
from ui import UIManager

class GameManager:
    def __init__(self, grid_size=(10, 6)):
        pygame.init()

        # Screen dimensions
        self.grid_size = grid_size
        self.tile_size = 64
        self.sidebar_width = 200
        self.screen_width = self.grid_size[0] * self.tile_size + self.sidebar_width
        self.screen_height = self.grid_size[1] * self.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("City Builder Simulation")

        # Game components
        self.clock = pygame.time.Clock()
        self.city = City(grid_size)
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.ui_manager = UIManager(self.screen, self.city, self.resource_manager)

        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.ui_manager.handle_event(event)

    def update(self):
        self.resource_manager.update(self.city)
        self.city.update()
        self.event_manager.update(self.city, self.resource_manager)

    def render(self):
        self.screen.fill((200, 200, 200))  # Light gray background
        self.ui_manager.render()
        pygame.display.flip()
