import random

class EventManager:
    def __init__(self):
        self.events = [
            {"name": "Earthquake", "effect": self.earthquake_effect},
            {"name": "Good Harvest", "effect": self.harvest_effect}
        ]

    def update(self, city, resource_manager):
        if random.random() < 0.02:  # 2% chance per frame
            event = random.choice(self.events)
            print(f"Event triggered: {event['name']}")
            event["effect"](city, resource_manager)

    def earthquake_effect(self, city, resource_manager):
        city.happiness -= 20

    def harvest_effect(self, city, resource_manager):
        resource_manager.resources['food'] += 50
