import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("City Builder Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
font = pygame.font.Font(None, 36)

# Game Variables
clock = pygame.time.Clock()
FPS = 60
resources = {"wood": 100}
buildings = []
game_data_file = "save_data.json"

# Load and scale images
def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        exit()

tree_image = load_image("assets/tree.png", (50, 50))
house_image = load_image("assets/house.png", (70, 70))

# Building types
building_types = [
    {"name": "Tree", "wood_cost": 0, "image": tree_image},
    {"name": "House", "wood_cost": 50, "image": house_image},
]

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 3)  # Border
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Functions
def draw_text(text, x, y, color=BLACK):
    """Draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def save_game():
    """Save the game data."""
    data = {
        "resources": resources,
        "buildings": [{"x": b["x"], "y": b["y"], "type": b["type"]} for b in buildings],
    }
    with open(game_data_file, "w") as f:
        json.dump(data, f)
    print("Game Saved!")

def load_game():
    """Load the game data."""
    if os.path.exists(game_data_file):
        with open(game_data_file, "r") as f:
            data = json.load(f)
            global resources, buildings
            resources = data.get("resources", resources)
            buildings.clear()
            for b in data.get("buildings", []):
                for bt in building_types:
                    if bt["name"] == b["type"]:
                        buildings.append({"x": b["x"], "y": b["y"], "type": b["type"], "image": bt["image"]})
            print("Game Loaded!")

def add_building(x, y, building_type):
    """Add a building if resources are sufficient."""
    if building_type["name"] != "Tree" and resources["wood"] < building_type["wood_cost"]:
        print("Not enough wood!")
        return

    if building_type["name"] != "Tree":
        resources["wood"] -= building_type["wood_cost"]

    buildings.append({"x": x, "y": y, "type": building_type["name"], "image": building_type["image"]})

def gather_resources():
    """Gather wood resources over time."""
    resources["wood"] += 1

# Create Buttons
buttons = [
    Button(10, 10, 150, 50, "Plant Tree", lambda: "Tree"),
    Button(10, 70, 150, 50, "Build House", lambda: "House"),
]

# Main Game Loop
running = True
load_game()

while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            save_game()
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            x, y = event.pos

            # Check if a button is clicked
            for button in buttons:
                if button.is_clicked((x, y)):
                    action = button.action()
                    if action in ["Tree", "House"]:
                        add_building(x, y, building_types[0 if action == "Tree" else 1])
                    break

    # Update Logic
    gather_resources()

    # Draw Resources
    draw_text(f"Wood: {resources['wood']}", 200, 20)

    # Draw Buttons
    for button in buttons:
        button.draw(screen)

    # Draw Buildings
    for building in buildings:
        screen.blit(building["image"], (building["x"], building["y"]))

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
