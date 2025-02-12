import pygame
from city import City
from resources import ResourceManager
from events import EventManager
from ui import UIManager

class GameManager:
    def __init__(self, grid_size=(10, 6)):
        pygame.init()
        self.grid_size = grid_size
        self.tile_size = 64
        self.sidebar_width = 200
        
        # Screen setup
        self.screen = pygame.display.set_mode(
            (grid_size[0] * self.tile_size + self.sidebar_width, 
             grid_size[1] * self.tile_size)
        )
        pygame.display.set_caption("City Builder Simulation")

        # Game components
        self.clock = pygame.time.Clock()
        self.city = City(grid_size)
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.ui_manager = UIManager(self.screen, self.city, self.resource_manager)

        # Timing control
        self.event_check_interval = 1.0
        self.event_check_timer = 0.0
        self.running = True

    def run(self):
        """Main game loop with delta time calculation"""
        last_time = pygame.time.get_ticks()
        while self.running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Delta time in seconds
            last_time = current_time

            self.handle_events()
            self.update(dt)
            self.render()
            self.clock.tick(60)  # Increased to 60 FPS for smoother updates

    def handle_events(self):
        """Handle input events efficiently"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                self.ui_manager.handle_event(event)

    def update(self, dt):
        """Update game state with time-based updates"""
        # Update resources every frame (if needed for animations)
        self.resource_manager.update(self.city)
        
        # Throttle expensive updates
        self.event_check_timer += dt
        if self.event_check_timer >= self.event_check_interval:
            self.event_check_timer = 0
            self.city.update()
            self.event_manager.update(self.city, self.resource_manager)

    def render(self):
        """Optimized rendering with static/dynamic separation"""
        self.ui_manager.render()
        pygame.display.update(self.ui_manager.get_dirty_areas())


# Optimized UIManager (partial implementation)
class UIManager:
    def __init__(self, screen, city, resource_manager):
        self.screen = screen
        self.city = city
        self.resource_manager = resource_manager
        self.static_drawn = False
        self.dirty_areas = []
        
        # Pre-cache static elements
        self.static_surface = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA)
        self._draw_static_elements()
        
        # Font caching
        self.font = pygame.font.Font(None, 24)
        self.cached_text = {}

    def _draw_static_elements(self):
        """Draw elements that don't change during gameplay"""
        # Grid background
        self.static_surface.fill((40, 40, 40))
        # Side panel
        sidebar_rect = pygame.Rect(
            self.city.grid_size[0] * 64, 0,
            self.sidebar_width, self.city.grid_size[1] * 64
        )
        pygame.draw.rect(self.static_surface, (30, 30, 30), sidebar_rect)
        self.static_drawn = True

    def render(self):
        """Efficient render with dirty rectangle tracking"""
        if not self.static_drawn:
            self.screen.blit(self.static_surface, (0, 0))
            self.dirty_areas.append(pygame.Rect(0, 0, *self.screen.get_size()))
            return

        # Draw dynamic elements
        self._draw_resources()
        self._draw_buildings()

    def _draw_resources(self):
        """Only redraw resource counters when they change"""
        resources = self.resource_manager.get_resources()
        text = f"Resources: {resources}"
        if text not in self.cached_text:
            self.cached_text[text] = self.font.render(text, True, (255, 255, 255))
        text_surface = self.cached_text[text]
        
        text_rect = text_surface.get_rect(topleft=(10, 10))
        if text_rect not in self.dirty_areas:
            self.screen.blit(self.static_surface, text_rect, text_rect)
            self.screen.blit(text_surface, text_rect)
            self.dirty_areas.append(text_rect)

    def get_dirty_areas(self):
        dirty = self.dirty_areas.copy()
        self.dirty_areas.clear()
        return dirty
